import time
from points import *
from get_pairs_within_distance import *
from utilities import *

if __name__ == '__main__':
    t0 = time.time()

    #
    # SET THE NUMBER OF POINTS
    num_points = int(10000000)
    current_file_path = os.path.abspath(__file__)

    #
    # SET THE BOX SIZE
    box_x_min, box_x_max = 0., 100.
    box_y_min, box_y_max = 0., 100.
    box_z_min, box_z_max = 0., 100.

    #
    # SET THE DISTANCE BETWEEN THE PAIRS
    radius = 1.

    #
    # SET THE FILE NAMES
    output_file_pts = "points.csv"
    output_file_close_pairs = "close_pairs.csv"


    #
    # NUMBER OF CHUNKS IN WHICH THE SET OF POINT IS DIVIDED
    # (along the x direction)
    n_of_chunks = 4


    #
    # DEFAULT CHUNK SIZE
    chunk_size = int(num_points / n_of_chunks + num_points / (2 * n_of_chunks))


    # delete the output file if it exists
    output_file_pts = os.path.dirname(current_file_path)+"/"+output_file_pts
    output_file_close_pairs = os.path.dirname(current_file_path)+"/"+output_file_close_pairs
    delete_file_if_exists(output_file_pts)
    delete_file_if_exists(output_file_close_pairs)

    print(f"Creating {num_points} points ...")
    points = generate_random_points_in_3d_box(num_points, box_x_min, box_x_max, box_y_min, box_y_max, box_z_min, box_z_max)

    # for testing
    # points =  np.asarray([[10.,0.,0.],[10.5,0.,0.],[49.1,0.,0.],[49.5,0.,0.],[50.4,0.,0.],[51.3,0.,0.],[79.,0.,0.],[79.5,0.,0.]])
    # points = np.asarray([[49.1, 0., 0.], [49.0, 0., 0.], [50., 0., 0.], [50.99999991, 0., 0.]])

    print(f"Writing points to file...")
    write_ascii_file(points, output_file_pts)

    # loop over the chunks of points (along the x direction)...
    for i in range(n_of_chunks):
        print(f"Chunk n. {i+1} of {n_of_chunks} ...")

        x_min = box_x_min + i * (box_x_max - box_x_min) / n_of_chunks
        x_max = box_x_min + (i+1) * (box_x_max - box_x_min) / n_of_chunks

        chunk_IDs = get_chunk_of_points(chunk_size, points, x_min, x_max)

        pairs = get_pairs_within_distance(points[chunk_IDs,:], radius)

        write_close_pairs_to_file(chunk_IDs[pairs]+1, output_file_close_pairs)

    # Iterate at the interfaces between chunks to find the remaining pairs
    toll = 1.5
    chunk_size = int(num_points * (2. * radius) / (box_x_max - box_x_min) * toll)

    for i in range(n_of_chunks-1):
        print(f"Interface n. {i+1} of {n_of_chunks-1} ...")

        x_interface = box_x_min + (i + 1) * (box_x_max - box_x_min) / n_of_chunks
        x_min = x_interface - radius
        x_max = x_interface + radius

        chunk_IDs = get_chunk_of_points(chunk_size, points, x_min, x_max)

        pairs = get_pairs_within_distance(points[chunk_IDs,:], radius)

        if pairs.size>0:

            # keep the pairs made of points located on opposite sides of the interface between two chunks of points
            pairs = remove_pairs_same_side(pairs, x_interface, points, chunk_IDs)

            write_close_pairs_to_file(chunk_IDs[pairs]+1, output_file_close_pairs)


    elapsed = time.time() - t0
    print(f"Executed in: {elapsed} s")

