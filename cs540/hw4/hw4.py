#!/usr/bin/env python
# coding: utf-8
# %%
from scipy.cluster.hierarchy import dendrogram
import numpy as np
from matplotlib import pyplot as plt
import csv

# talked with Zhiqi about using a 2d array for distance matrix instead of dictonary, 
# asked chat GBT how to make a distanc matrix from features
#asked chat gbt how to imporve my normlize function, I wanted to see if there was a better way

# %%
# read in file
def load_data(filepath):
    file = open(filepath, encoding="utf-8")
    csv_data = csv.DictReader(file)
    country_list = []
    for row in csv_data:
        row_data = {}
        for key in row:
            row_data[key] = row[key]
        country_list.append(row_data)
        
    file.close()
    return country_list


# %%
# get features from row
def calc_features(row):
    row_list = []
    for key in row:
        if key == "" or key == "Country":
            continue
        row_list.append(row[key])
    
    return np.array(row_list, dtype=np.float64)


# %%
# calculate euclidean distance 
# sqrt((x-x)**2 + ... (x-x)**2)
def calc_euclidean_distances(v1, v2):
    if len(v1) != len(v2):
        return None
    total = 0
    for i in range(len(v1)):
        total += (v1[i] - v2[i])**2
    return total ** 0.5


# %%
# create the distance matrix with calc_euclidean_distances function
def create_dist_matrix(features):
    n = len(features)
    distance_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i + 1, n):
            distance_matrix[i][j] = calc_euclidean_distances(features[i], features[j])
            distance_matrix[j][i] = distance_matrix[i, j] 
    return distance_matrix


# %%
# find next clusters to merge
def get_next_cluster(distance_matrix, clusters):
    # initlize values
    current_min = np.inf
    v1 = -1
    v2 = -1
    for i in range(len(clusters)):
        for j in range(i+1, len(clusters)):
            # check for -1 (removed cluster) or 0 (looking at same clusters)
            if distance_matrix[i][j] == -1 or distance_matrix[i][j] == 0:
                continue
            # check for min
            if distance_matrix[i][j] < current_min:
                current_min = distance_matrix[i][j]
                v1 = i
                v2 = j
    return (v1, v2)


# %%
# update distqance matrix after merged clsuter
def update_distance_matrix(matrix, v1, v2, n):
    # add extra coulmn and row
    matrix = np.vstack((matrix, np.zeros((1, n))))
    matrix = np.hstack((matrix, np.zeros((n+1, 1))))
    # loop
    for i in range(len(matrix)):
        # make sure we aren't at a coulmn we are merging
        if i != v1 or i != v2:
            # check for min and make symetric
            matrix[i][n] = min(matrix[i][v1], matrix[i][v2])
            matrix[n][i] = matrix[i][n]
    # set to -1
    matrix[v1, :] = -1
    matrix[v2, :] = -1
    matrix[:, v1] = -1
    matrix[:, v2] = -1
    
    return matrix    



# %%
# count countries in cluster
def count_countries(v1, clusters):
    total = 0
    for i in range(len(clusters[v1])):
        # check int, add
        if type(clusters[v1][i]) == int:
            total +=1
        # check tuple, call count_countries on tuple
        elif type(clusters[v1][i]) == tuple:
            total += count_countries(clusters[v1][i])
    return total


# %%
# normilize values to (x - col_min) / (col_max - col_min)
def normalize_features(features):
    # inistialize lists
    col_1 = []
    col_2 = []
    col_3 = []
    col_4 = []
    col_5 = []
    col_6 = []
    
    # add all features
    for i in range(len(features)):
        col_1.append(features[i][0])
        col_2.append(features[i][1])
        col_3.append(features[i][2])
        col_4.append(features[i][3])
        col_5.append(features[i][4])
        col_6.append(features[i][5])
    
    # find maxes and mins
    col_1_max =max(col_1)
    col_1_min =min(col_1)
    col_2_max =max(col_2)
    col_2_min =min(col_2)
    col_3_max =max(col_3)
    col_3_min =min(col_3)
    col_4_max =max(col_4)
    col_4_min =min(col_4)
    col_5_max =max(col_5)
    col_5_min =min(col_5)
    col_6_max =max(col_6)
    col_6_min =min(col_6)
    
    # normilize
    for i in range(len(features)):
        features[i][0] = (features[i][0] - col_1_min) / (col_1_max - col_1_min)
        features[i][1] = (features[i][1] - col_2_min) / (col_2_max - col_2_min)
        features[i][2] = (features[i][2] - col_3_min) / (col_3_max - col_3_min)
        features[i][3] = (features[i][3] - col_4_min) / (col_4_max - col_4_min)
        features[i][4] = (features[i][4] - col_5_min) / (col_5_max - col_5_min)
        features[i][5] = (features[i][5] - col_6_min) / (col_6_max - col_6_min)
    
    return features


# %%
# preform heirnacry aggromutive clustering
def hac(features):
    # set up needed structures
    n = len(features)
    Z = []
    clusters = []
    distance_matrix = create_dist_matrix(features)
    
    # set each item to a cluster by itself
    for i in range(n):
        clusters.append([i])
    
    # loop
    for i in range(n-1):
        Z_i = []
        # find next pair
        v1, v2 = get_next_cluster(distance_matrix, clusters)
        # append pairs to Z and distance
        Z_i.append(v1)
        Z_i.append(v2)
        Z_i.append(distance_matrix[v1][v2])
        # add pair to clusters
        clusters.append(clusters[v1] + clusters[v2])
        # add total number in cluster
        Z_i.append(count_countries(v1, clusters) + count_countries(v2, clusters))
        Z.append(Z_i)
        # update distance matrix
        distance_matrix = update_distance_matrix(distance_matrix, v1, v2, n-1+i+1)

        
    return np.array(Z)


# %%
# dispaly dendrogram of clusters
def fig_hac(Z, names):
    fig = plt.figure()
    dn = dendrogram(Z, labels = names, leaf_rotation = 90)
    return fig


# %%
data = load_data("countries.csv")
country_names = [row["Country"] for row in data]
features = [calc_features(row) for row in data]
features_normalized = normalize_features(features)
n = 50
Z_raw = hac(features[:n])
Z_normalized = hac(features[:n])
fig = fig_hac(Z_raw, country_names[:n])
plt.show()
