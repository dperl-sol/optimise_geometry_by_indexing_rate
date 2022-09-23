#!/usr/bin/env python3

import helper_functions
import numpy as np
import logging
logging.basicConfig(filename='log.txt',level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())
import argparse
import json
import copy
import os
import subprocess
from operator import add

def get_args():
    parser = argparse.ArgumentParser(description='Refine a beam centre and/or detector distance based on the indexing rate over a grid of points')
    parser.add_argument('input_hdf5',help='hdf5 file to refine on')
    parser.add_argument('input_geom',help='expt file with original geometry')
    parser.add_argument('input_phil',help='phil file for cctbx.small_cell indexing instructions')
    parser.add_argument('-r', '--n_rows', help='Number of grid points in y direction', type=int, default=0)
    parser.add_argument('-c', '--n_columns', help='Number of grid points in x direction', type=int, default=0)
    parser.add_argument('-d', '--n_distance', help='Number of grid points in detector distance', type=int, default=0)
    parser.add_argument('-x','--y_increment', help='Grid point increment in y direction in mm', type=float, default=0.01)
    parser.add_argument('-y','--x_increment', help='Grid point increment in x direction in mm', type=float, default=0.01)
    parser.add_argument('-s','--d_increment', help='Grid point increment in detector distance in mm', type=float, default=0.05)
    parser.add_argument('-n', '--n_cores', help='Number of cores to use for cctbx.small_cell_process', type=int, default=64)
    return parser.parse_args()

def make_and_write_expts(input_expt, n_x:int, n_y:int, n_d:int, i_x:float, i_y:float, i_d:float):
    """ Write DIALS .expt files with modified detector geometry,
    and return the filenames written as a list of strings.
    Takes a template .expt file to modify, and the number of points
    and increment size in mm in x, y, and detector distance directions.
    """
    points_x, points_y, points_d = helper_functions.calculate_points(n_x, n_y, n_d, i_x, i_y, i_d)
    files = []
    for x in range(n_x):
        for y in range(n_y):
            for d in range(n_d):
                logging.info("Preparing geometry file with modifications of (x,y,d): ("+str(points_x[x])+','+str(points_y[y])+','+str(points_d[d])+')')
                # for deployment:
                # if not os.path.isdir('geoms'): os.makedirs('geoms')
                # filename = 'geoms/'+str(x)+'_'+str(y)+'_'+str(d)+'.expt'
                #
                # for writing and debugging:
                filename = 'testdata/geoms/'+str(x)+'_'+str(y)+'_'+str(d)+'.expt'
                modified_expt = copy.copy(input_expt)
                modified_expt['detector'][0]['panels'][0]['origin'] = list(map( add, 
                                                                                input_expt['detector'][0]['panels'][0]['origin'], 
                                                                                [points_x[x], points_y[y], points_d[d]] ))
                logging.info(str(modified_expt['detector'][0]['panels'][0]['origin']))
                logging.info("writing to file: "+filename+'\n')
                files.append(filename)
                with open(filename, 'w') as f:
                    json.dump(modified_expt, f, indent=2)
                
    return files

def execute_indexing_run(philfile:str, datafile:str, geomfile:str, cores:int=16):
    """ Execute a cctbx.small_cell_process run on the specified data file,
    using the settings from a DIALS .phil file and the .expt geometry file
    for the input.reference_geometry option. Multiprocessing with the specified
    number of cores (default 16.)
    """
    out_folder = geomfile[:-5]+'_out'
    log_folder = geomfile[:-5]+'_log'
    mpi_cmd = ['mpirun','-n',str(cores),'cctbx.small_cell_process',philfile, datafile, f'output.output_dir={out_folder}',
                f'output.logging_dir={log_folder}', f'input.reference_geometry={geomfile}', 'mp.method=mpi']
    logging.info("running mpirun with args: ")
    logging.info(' '.join(mpi_cmd))

    if not os.path.isdir(out_folder): os.makedirs(out_folder)
    if not os.path.isdir(log_folder): os.makedirs(log_folder)
    subprocess.run(mpi_cmd)


def main():
    args = get_args()
    with open(args.input_geom) as f:
        initial_geometry = json.load(f)
    runs = make_and_write_expts(initial_geometry, 
                                args.n_columns,
                                args.n_rows,
                                args.n_distance,
                                args.x_increment,
                                args.y_increment,
                                args.d_increment)
    
    n_cores = 16
    if args.n_cores is not None: n_cores = args.n_cores
    for geomfile in runs:
        execute_indexing_run(args.input_phil, args.input_hdf5, geomfile, cores=n_cores)



if __name__ == '__main__':
    main()
