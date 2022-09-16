#!/usr/bin/env python
import h5py
import numpy as np
import logging
logging.basicConfig(filename='log.txt',level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())
import argparse
import matplotlib as mpl
import json

def get_args():
    parser = argparse.ArgumentParser(description='Refine a beam centre and/or detector distance based on the indexing rate over a grid of points')
    parser.add_argument('input_hdf5',help='hdf5 file to refine on')
    parser.add_argument('input_geom',help='expt file with original geometry')
    parser.add_argument('input_phil',help='phil file for cctbx.small_cell indexing instructions')
    parser.add_argument('-t', '--n_height', help='Number of grid points in y direction', type=int, default=0)
    parser.add_argument('-w', '--n_width', help='Number of grid points in x direction', type=int, default=0)
    parser.add_argument('-d', '--n_distance', help='Number of grid points in detector distance', type=int, default=0)
    parser.add_argument('-x','--y_increment', help='Grid point increment in y direction', type=float, default=0.01)
    parser.add_argument('-y','--x_increment', help='Grid point increment in x direction', type=float, default=0.01)
    parser.add_argument('-s','--d_increment', help='Grid point increment in detector distance', type=float, default=0.05)
    parser.add_argument('-n', '--n_cores', help='Number of cores to use for cctbx.small_cell_process', type=int, default=64)
    return parser.parse_args()

def make_expts(input_expt, n_x, n_y, n_d, i_x, i_y, i_s):
    if n_x == 0:
        n_x = 1
        i_x = 0
        points_x = [0]
    else: points_x = np.arange(-n_x*i_x/2,n_x*i_x/2,i_x)
    if n_y == 0:
        n_y = 1
        i_y = 0
        points_y = [0]
    else: points_y = np.arange(-n_y*i_y/2,n_y*i_y/2,i_y)
    if n_d == 0:
        n_d = 1
        i_d = 0
        points_d = [0]
    else: points_d = np.arange(-n_d*i_d/2,n_d*i_d/2,i_d)
    coords_for_new_geoms_to_make = []
    for x in range(n_x):
        for y in range(n_y):
            for d in range(n_d):
                coords_for_new_geoms_to_make.append((points_x[x],points_y[y],points_d[d]))
    logging.info("Preparing geometry files with modifications of (x,y,d): ")
    logging.info(str(coords_for_new_geoms_to_make))

def main():
    args = get_args()
    initial_geometry = json.load(args.input_geom)
    make_expts("test",  args.n_width,
                        args.n_height,
                        args.n_distance,
                        args.x_increment,
                        args.y_increment,
                        args.d_increment)



if __name__ == '__main__':
    main()
