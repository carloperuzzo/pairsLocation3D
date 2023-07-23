import random
import numpy as np


def generate_random_points_in_3d_box(num_points, x_min, x_max, y_min, y_max, z_min, z_max):

    points = np.ndarray(shape=(num_points,3))
    i = 0
    while i < num_points:
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        z = random.uniform(z_min, z_max)
        points[i,0]=x;points[i,1]=y;points[i,2]=z
        i=i+1
    return points


def get_chunk_of_points(chunk_size, points, x_min, x_max):
    # slice the cloud of points along the x coordinate
    # take all the points in a box beteween x_min and x_max
    chunk_IDs = np.empty(chunk_size,dtype=int)
    count = 0
    for i, p in enumerate(points):
        if count < chunk_size :
            if p[0] >= x_min and p[0] < x_max:
                    chunk_IDs[count] = i
                    count +=1
        else:
            # chunk_margin_to_be_increased
            print("ERROR: increase the chunk size!")
            return None

    # all good!
    return chunk_IDs[0:count]


def remove_pairs_same_side(pairs, x_interface, points, chunk_IDs):
    # keep the pairs made of points located on opposite sides of the interface between two chunks of points
    points_local = points[chunk_IDs, :]
    pairs_filtered_ID = np.empty(pairs.size, dtype=int)
    count = 0
    for j, p in enumerate(pairs):
        condition_1 = (points_local[p[0]][0] < x_interface and points_local[p[1]][0] >= x_interface)
        condition_2 = (points_local[p[0]][0] > x_interface and points_local[p[1]][0] <= x_interface)
        if condition_1 or condition_2:
            pairs_filtered_ID[count] = j
            count += 1
    pairs = pairs[pairs_filtered_ID[0:count]]
    return pairs