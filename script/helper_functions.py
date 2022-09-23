def calculate_points(n_x:int, n_y:int, n_d:int, i_x:float, i_y:float, i_d:float):
    if n_x == 0:
        n_x = 1
        i_x = 0
        points_x = [0]
    else: 
        points_x = np.arange(-(n_x-1)*i_x/2,(n_x+1)*i_x/2,i_x)
        #if (n_x % 2 == 0): points_x = points_x[:-1]
    if n_y == 0:
        n_y = 1
        i_y = 0
        points_y = [0]
    else: 
        points_y = np.arange(-(n_y-1)*i_y/2,(n_y+1)*i_y/2,i_y)
        #if (n_y % 2 == 0): points_y = points_y[:-1]
    if n_d == 0:
        n_d = 1
        i_d = 0
        points_d = [0]
    else: 
        points_d = np.arange(-(n_d-1)*i_d/2,(n_d+1)*i_d/2,i_d)
        #if (n_d % 2 == 0): points_d = points_y[:-1]
    return(points_x,points_y,points_d)