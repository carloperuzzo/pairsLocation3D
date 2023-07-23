import os


def delete_file_if_exists(file_path):

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted successfully.")
        except OSError as e:
            print(f"Error occurred while deleting '{file_path}': {e}")
    else:
        print(f"File '{file_path}' does not exist.")



def write_ascii_file(points, output_file):

    with open(output_file, 'w') as f:
        #f.write("Index, X, Y, Z\n")
        for i, (x, y, z) in enumerate(points, start=1):
            f.write(f"{i}, {x}, {y}, {z}\n")



def write_close_pairs_to_file(close_pairs, output_file):

    with open(output_file, 'a') as f:
        #f.write("Point 1, Point 2\n")
        for p1, p2 in close_pairs:
            f.write(f"{p1}, {p2}\n")