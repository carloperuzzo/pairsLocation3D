from scipy.spatial import KDTree

# This function builds a kd_tree and returns the points within the radius
def get_pairs_within_distance(points, radius):
    kd_tree = KDTree(points)
    return kd_tree.query_pairs(r=radius, output_type='ndarray')