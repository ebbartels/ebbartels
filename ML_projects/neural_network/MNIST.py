# +
import torch

import pandas as pd
import zipfile
import os
import gzip
import matplotlib.pyplot as plt
import numpy as np
# -

# !kaggle datasets download -d hojjatk/mnist-dataset 


with zipfile.ZipFile("mnist-dataset.zip", 'r') as zip_ref:
    zip_ref.extractall("mnist-dataset")


def load_idx_gz(filename):
    with gzip.open(filename, 'rb') as f:
        # Read the magic number (first 4 bytes)
        magic = int.from_bytes(f.read(4), byteorder='big')
        print(f"Magic number: {magic}")
        
        # Read dimensions
        num_images = int.from_bytes(f.read(4), byteorder='big')
        rows = int.from_bytes(f.read(4), byteorder='big')
        cols = int.from_bytes(f.read(4), byteorder='big')
        
        print(f"Number of images: {num_images}, Rows: {rows}, Columns: {cols}")
        
        # Read the rest of the data as a NumPy array
        buffer = f.read()
        data = np.frombuffer(buffer, dtype=np.uint8)
        
        # Reshape data into images
        data = data.reshape(num_images, rows, cols)
        
        return data



# +
import gzip
import numpy as np

def load_idx_labels_gz(filename):
    with gzip.open(filename, 'rb') as f:
        # Read the magic number (first 4 bytes)
        magic = int.from_bytes(f.read(4), byteorder='big')
        print(f"Magic number: {magic}")
        
        # Read number of items (labels)
        num_labels = int.from_bytes(f.read(4), byteorder='big')
        print(f"Number of labels: {num_labels}")
        
        # Read the rest of the data as a NumPy array (dtype is uint8 for labels)
        buffer = f.read()
        labels = np.frombuffer(buffer, dtype=np.uint8)
        
        return labels



# -

train_images_path = os.path.join("data","MNIST", "raw", "train-images-idx3-ubyte.gz")
train_images = load_idx_gz(train_images_path)


path_label_train = os.path.join("data","MNIST", "raw", "train-labels-idx1-ubyte.gz")
train_labels = load_idx_labels_gz(path_label_train)

test_images_path = os.path.join("data","MNIST", "raw", "t10k-images-idx3-ubyte.gz")
test_images = load_idx_gz(test_images_path)

test_labels_path = os.path.join("data","MNIST", "raw", "t10k-labels-idx1-ubyte.gz")
test_labels = load_idx_labels_gz(test_labels_path)
