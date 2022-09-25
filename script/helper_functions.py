import numpy as np

def calculate_points(n_x:int, n_y:int, n_d:int, i_x:float, i_y:float, i_d:float):
    if n_x == 0 or n_x == 1:
        n_x = 1
        i_x = 0
        points_x = [0]
    else: 
        if n_x % 2 == 1: points_x = np.linspace((-(n_x - 1)/2.0)*i_x, ((n_x - 1)/2.0)*i_x, n_x)
        else: points_x = np.linspace(-(n_x/2.0)*i_x, (n_x/2.0)*i_x, n_x)
    if n_y == 0 or n_y == 1:
        n_y = 1
        i_y = 0
        points_y = [0]
    else: 
        points_y = np.linspace(-(n_y)*i_y/2, (n_y)*i_y/2, n_y)
        if n_y % 2 == 1: points_y = np.linspace((-(n_y - 1)/2.0)*i_y, ((n_y - 1)/2.0)*i_y, n_y)
        else: points_y = np.linspace(-(n_y/2.0)*i_y, (n_y/2.0)*i_y, n_y)
    if n_d == 0 or n_d == 1:
        n_d = 1
        i_d = 0
        points_d = [0]
    else: 
        points_d = np.linspace(-(n_d)*i_d/2, (n_d)*i_d/2, n_d)
        if n_d % 2 == 1: points_d = np.linspace((-(n_d - 1)/2.0)*i_d, ((n_d - 1)/2.0)*i_d, n_d)
        else: points_d = np.linspace(-(n_d/2.0)*i_d, (n_d/2.0)*i_d, n_d)
    return(points_x,points_y,points_d)