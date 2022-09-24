#!/usr/bin/env python3

from symbol import parameters
import helper_functions
import matplotlib.pyplot as plt
import os
import subprocess
import numpy as np
import json

def get_args():
    parser = argparse.ArgumentParser(description='Analyse the results of detector position refinement and display results.')
    parser.add_argument('input_json', help='json file generated by optimise_geometry_by_indexing_rate.py with processing parameters.')
    return parser.parse_args()

def display_2d_results(data, n_a:int, n_b:int, i_a:float, i_b:float):
    """ Display results as a pixel-plot with a colorramp corresponding to the number of indexed images
    at each position.
    """
    a_extent = i_a*float(n_a)/2
    b_extent = i_b*float(n_b)/2
    aticks, bticks, cticks = helper_functions.calculate_points(n_a, n_b, 0, i_a, i_b, 0)
    pixel_plot = plt.figure()
    pixel_plot.add_axes()
    plt.title('indexing results by detector origin translation')
    pixel_plot = plt.imshow(data,extent=[-a_extent, a_extent, -b_extent, b_extent])
    plt.xticks(aticks)
    plt.yticks(bticks)
    plt.colorbar(pixel_plot)
    plt.show()


def load_results_from_folders(dims):
    """ In the absence of a file with proper parameters, attempt to look at the output folders.
    """
    outfolders = [x for x in os.listdir('..') if x.endswith('out')]
    images_indexed = []
    for f in outfolders:
        print(f)
        imgs = subprocess.run(['grep real_space_a ../'+f+'/*refined.expt | wc -l'],shell=True,capture_output=True)
        print(int(imgs.stdout.decode()))
        images_indexed.append(int(imgs.stdout.decode()))

    grid = np.reshape(images_indexed, dims, order='F')
    names = np.reshape(outfolders, dims, order='F')

    return grid

def main():
    os.chdir('/nfs/data2/2022_Run4/com-proxima2a/2022-09-11/RAW_DATA/IHR/David/GasCell/MUF16_CO2/single_test_wedges/1_2_bar/process/optimise_geom/grid_7by7/analysis')
    with open('parameters.json') as f:
        parameters = json.load(f)
    
    dims = (parameters['n_x'],parameters['n_y'],parameters['n_d'])
    incrs = (parameters['i_x'],parameters['i_y'],parameters['i_d'])
    data = np.squeeze(load_results_from_folders(dims))

    if dims[2] == 1:
        display_2d_results(data, dims[0], dims[1], incrs[0], incrs[1])

if __name__ == '__main__':
    main()