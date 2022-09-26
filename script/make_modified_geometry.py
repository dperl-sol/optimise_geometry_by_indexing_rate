#!/usr/bin/env python3

import helper_functions
import json
import argparse
import copy
from operator import add

def get_args():
    parser = argparse.ArgumentParser(description='Make a modified geometry file.')
    parser.add_argument('input_geom', help='DIALS .expt file to load')
    parser.add_argument('output_geom', help='new DIALS .expt file to write')
    parser.add_argument('--shift', nargs=3, type=float, help='detector shift in mm, 3 floats: x y d', required=True)
    return parser.parse_args()

def main():
    args = get_args()

    shift = args.shift
    with open(args.input_geom) as f:
        initial_geometry = json.load(f)
    initial_geometry = helper_functions.clean_initial_geometry(initial_geometry)
    
    logging.info("Preparing geometry file with modifications of (x,y,d): ("+str(shift[0])+','+str(shift[1])+','+str(shift[2])+')')
    logging.info('Starting origin: '+str(initial_geometry['detector'][0]['panels'][0]['origin']))
    
    modified_geometry = copy.deepcopy(initial_geometry)
    old_point = initial_geometry['detector'][0]['panels'][0]['origin']
    new_point = list(map(add, old_point, shift))
    logging.info('New origin: '+str(new_point))
    modified_geometry['detector'][0]['panels'][0]['origin'] = new_point
    
    logging.info("writing to file: "+args.output_geom+'\n')
    with open(args.output_geom, 'w') as f:
        json.dump(modified_geometry, f, indent=2)
    

if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='log.txt',level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
    main()