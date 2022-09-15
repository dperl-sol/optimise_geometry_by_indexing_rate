#!/usr/bin/env python
import h5py
import numpy as np
import logging
import argparse
import matplotlib as mpl
import json

def get_args():
    parser = argparse.ArgumentParser(description='Refine a beam centre and/or detector distance based on the indexing rate over a grid of points')
    parser.add_argument('input_hdf5',help='hdf5 file to refine on')
    parser.add_argument('input_geom',help='expt file with original geometry')
    parser.add_argument('input_phil',help='phil file for cctbx.small_cell indexing instructions')
    parser.add_argument('-h', '--n_height', help='Number of grid points in y direction', type=int, default=0)
    parser.add_argument('-w', '--n_width', help='Number of grid points in x direction', type=int, default=0)
    parser.add_argument('-d', '--n_distance', help='Number of grid points in detector distance', type=int, default=0)
    parser.add_argument('-x','--y_increment', help='Grid point increment in y direction', type=float, default=0.01)
    parser.add_argument('-y','--x_increment', help='Grid point increment in x direction', type=float, default=0.01)
    parser.add_argument('-s','--d_increment', help='Grid point increment in detector distance', type=float, default=0.05)
    parser.add_argument('-n', '--n_cores', help='Number of cores to use for cctbx.small_cell_process', type=int, default=64)
    return parser.parse_args()

def main():
    args = get_args()
    do_x = args['n_width'] != 0
    do_y = args['n_height'] != 0
    do_s = args['n_distance'] != 0



if __name__ == '__main__':
    main()
