import sys
import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Define the hashbits.
b = 64


def hamming_distance(hash1, hash2):
    x = (hash1 ^ hash2) & ((1 << b) - 1)
    distance = 0
    while x:
        distance += 1
        # reset the last non zero bit to 0
        x &= x - 1
    return distance

# The simHash function in the paper refer to the implementation of python-hashes
# python-hashes: (https://github.com/sean-public/python-hashes/blob/master/hashes/simhash.py)


def create_hash(feature):
    v = [0] * b
    for t in [(string_hash(k), v) for k, v in feature.items()]:
        bitmask = 0
        for i in range(b):
            bitmask = 1 << i
            if t[0] & bitmask:
                v[b - i - 1] += t[1]
            else:
                v[b - i - 1] += -1 * t[1]

    fingerprint = 0
    for i in range(b):
        if v[i] >= 0:
            fingerprint += 1 << i
    return fingerprint


def string_hash(v):
    if v == "":
        return 0
    else:
        x = ord(v[0]) << 7
        m = 100003
        mask = 2 ** b - 1
        for c in v:
            x = ((x*m) ^ ord(c)) & mask
        x ^= len(v)
        if x == -1:
            x = -2
        return x


def SimHash(h, h_hat):
    return 1 - hamming_distance(h, h_hat) / b


def compute_similarity(feature1, feature2):
    u = create_hash(feature1)
    v = create_hash(feature2)
    return SimHash(u, v)


def compute_features(graph):
    # Get pagerank of vertices
    pagerank = nx.pagerank(graph)

    # Compute edges quality
    weighted_features = {}
    for edge in graph.edges():
        u, v = edge[0], edge[1]
        key = str(u) + "_" + str(v)
        weighted_features[key] = pagerank[u] / len(graph.edges(u))

    return weighted_features


def compute_threshold(results):
    n = len(results)
    sumMi = 0
    for i in range(1, n):
        Mi = abs(results[i] - results[i - 1])
        sumMi = sumMi + Mi
    M = sumMi / (n - 1)
    median = np.median(results)
    threshold = (median - 3 * M, median + 3 * M)
    return threshold


def read_graph(name):
    file_path = os.getcwd() + '/datasets/' + name

    # Read all files in the directory and create a networkx graph for each file
    graphes = []
    for file in os.listdir(file_path):
        file = file_path + '/' + file
        f = open(file, 'r')

        # Skip the first row containing number of nodes and edges
        next(f)

        # Create graph
        g = nx.Graph()
        for line in f:
            line = line.split()
            g.add_edge(int(line[0]), int(line[1]))

        # Add the graph into the graph list
        graphes.append(g)

    return graphes


def plot_timeseries(results, threshold, dataset):
    plt.plot(results)
    plt.axhline(y=threshold[0], color='r')
    plt.axhline(y=threshold[1], color='g')
    plt.ylabel('Similarity')
    plt.xlabel('Time')
    plt.title('Anomaly detection of' + dataset + 'dataset')
    plt.savefig(dataset + "_time_series.png")


def save_file(results, dataset):
    filename = dataset + "_time_series.txt"
    f = open(filename, 'w+')
    for res in results:
        f.write(str(res) + '\n')
    f.close()


def main():
    # Input validation
    if len(sys.argv) != 2:
        print("The input format is not proper ! Please enter as python anomaly.py <dataset directory containing one dataset>")
        exit(1)
    dataset = sys.argv[1]

    # Read the time series graphes from files
    print("Reading graphes.......")
    graphs = read_graph(dataset)

    # Get weighted features
    print("Computing weighted features.......")
    weighted_features = [compute_features(g) for g in graphs]

    # Compute Similarities
    print("Computing similarities of graphes.......")
    similarities = []
    for i in range(len(graphs) - 1):
        sim = compute_similarity(weighted_features[i], weighted_features[i+1])
        similarities.append(sim)

    # Compute threshold
    print("Computing threshold.......")
    threshold = compute_threshold(similarities)
    print("Threshold: {}".format(threshold))

    # Plot time series result
    print("Wrapping up time series result......")
    plot_timeseries(similarities, threshold, dataset)
    save_file(similarities, dataset + "_time_series.txt")

    print("Anomaly detection finished............")


# Call the main. Entry point.
if __name__ == "__main__":
    main()
