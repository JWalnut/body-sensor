import numpy as np

def split_and_stitch(data_mat, split_range=[]): # note: indices are inclusive on both ends
    if split_range == [] or len(split_range) % 2 != 0:
        return
    final_size = 0
    index = 0
    while True:
        final_size += split_range[index + 1] - split_range[index] + 1
        index += 2
        if index >= len(split_range):
            break
    out_mat = np.zeros((data_mat.shape[0], final_size))
    index = 0
    last_index = 0

    while True:
        size = split_range[index + 1] - split_range[index] + 1
        out_mat[:, last_index:last_index+size] = data_mat[:, split_range[index]:split_range[index + 1] + 1]
        last_index = last_index+size
        index += 2
        if index >= len(split_range):
            break
    return out_mat
