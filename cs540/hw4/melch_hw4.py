from scipy.cluster.hierarchy import linkage, dendrogram
import numpy as np
import csv
import matplotlib.pyplot as plt

def load_data(filepath):
    file = open(filepath, encoding="utf-8")
    csv_data = csv.DictReader(file)
    data_list = []
    for row in csv_data:
        stat_data = {}
        stat_data["HP"] = row["HP"]
        stat_data["Attack"] = row["Attack"]
        stat_data["Defense"] = row["Defense"]
        stat_data["Sp. Atk"] = row["Sp. Atk"]
        stat_data["Sp. Def"] = row["Sp. Def"]
        stat_data["Speed"] = row["Speed"]
        data_list.append(stat_data)
    file.close()
    return data_list

def calc_features(row):
    toReturn = []
    toReturn.append(row["Attack"])
    toReturn.append(row["Sp. Atk"])
    toReturn.append(row["Speed"])
    toReturn.append(row["Defense"])
    toReturn.append(row["Sp. Def"])
    toReturn.append(row["HP"])
    return np.array(toReturn, dtype=np.int64)

def hac(features):
    n = len(features)
    Z = list()
    clusters = init_clusters(features)
    dist_mtrx = create_dist_mtrx(features)
    for i in range(n - 1):
        Z.append([])
        next_cluster = get_next_cluster(dist_mtrx)
        c1 = min(next_cluster)
        c2 = max(next_cluster)
        Z[i].append(c1)
        Z[i].append(c2)
        Z[i].append(dist_mtrx[c1][c2])
        Z[i].append(count_pokemon(clusters, c1, c2))
        Z[i] = np.array(Z[i])
        update_clusters(clusters, c1, c2, (n-1) + (i+1))
        update_dist_mtrx(features, dist_mtrx, clusters, c1, c2, ((n-1) + (i+1)))
    return np.array(Z)

def imshow_hac(Z):
    fig = plt.figure(figsize=(25, 10))
    dn = dendrogram(Z)
    plt.show()

#Computes Euclidean distance between two vectors of the same size
def euclidean_dist(v1, v2):
    if len(v1) != len(v2):
        return None
    total = 0
    for i in range(len(v1)):
        total += (v1[i] - v2[i])**2
    return np.sqrt(total)

# Creates the starting distance mtrx for n feature vectors
# Inits with only lower triagnular values
def create_dist_mtrx(vectors):
    mtrx = dict()
    for i in range(len(vectors)):
        distances = dict()
        for j in range(i+1, len(vectors)):
            distances[j] = euclidean_dist(vectors[i], vectors[j])
        mtrx[i] = distances
    return mtrx

# Updates distance matrix by removing clusters passed in
# and calculating new complete-linkage distances
def update_dist_mtrx(features, dist_mtrx, clusters, c1, c2, new_id):
    del dist_mtrx[c1]
    del dist_mtrx[c2]
    for i in dist_mtrx.keys():
        if c1 in dist_mtrx[i]:
            del dist_mtrx[i][c1]
        if c2 in dist_mtrx[i]:
            del dist_mtrx[i][c2]
    for i in dist_mtrx.keys():
        dist_mtrx[i][new_id] = complete_linkage_dist(features, clusters, i, new_id)
    dist_mtrx[new_id] = dict() 
    return None

# Calculates the complete linkage distance between two clusters
def complete_linkage_dist(features, clusters, c1, c2):
    curr_max = 0
    if type(clusters[c1]) == int:
        for k in clusters[c2]:
            if euclidean_dist(features[c1], features[k]) > curr_max:
                    curr_max = euclidean_dist(features[c1], features[k])
    else:
        for i in clusters[c1]:
            for j in clusters[c2]:
                if euclidean_dist(features[i], features[j]) > curr_max:
                    curr_max = euclidean_dist(features[i], features[j])
    return curr_max

# Creates a dictionary containing each cluster ID and
# the features in that cluster
def init_clusters(features):
    clusters = dict()
    for i in range(len(features)):
        clusters[i] = i
    return clusters

# Updates clusters dict to have new cluster and remove old
# and update the new cluster with the old clusters' features
def update_clusters(clusters, c1, c2, id):
    clust_features = []
    if type(clusters[c1]) == int:
        clust_features.append(clusters[c1])
    else:
        clust_features = clust_features + clusters[c1]
    if type(clusters[c2]) == int:
        clust_features.append(clusters[c2])
    else:
        clust_features = clust_features + clusters[c2]
    del clusters[c1]
    del clusters[c2]
    clusters[id] = []
    clusters[id] = clusters[id] + clust_features
    return None

# Finds the next cluster to be added by
# minimum distance in current distance matrix
def get_next_cluster(dist_mtrx):
    v1 = 0
    v2 = 0
    curr_min = None
    for i in dist_mtrx.keys():
        for j in dist_mtrx[i].keys():
            if curr_min == None:
                curr_min = dist_mtrx[i][j]
                v1 = i
                v2 = j
            elif dist_mtrx[i][j] == curr_min:
                if v1 < i:
                    continue
                elif i > v1:
                    curr_min = dist_mtrx[i][j]
                    v1 = i
                    v2 = j
                elif v1 == i:
                    if v2 < j:
                        continue
                    else:
                        curr_min = dist_mtrx[i][j]
                        v1 = i
                        v2 = j
            elif dist_mtrx[i][j] < curr_min:
                curr_min = dist_mtrx[i][j]
                v1 = i
                v2 = j
    return (v1, v2)

# Calculates the number of pokemon in a new cluster
def count_pokemon(clusters, c1, c2):
    count_pkm = 0
    if type(clusters[c1]) == int:
        count_pkm += 1
    else:
        count_pkm += len(clusters[c1])
    if type(clusters[c2]) == int:
        count_pkm += 1
    else:
        count_pkm += len(clusters[c2])
    return count_pkm
