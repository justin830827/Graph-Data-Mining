import sys
import os
from igraph import *
import numpy as np
import numpy.linalg as la
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import warnings

__author__ = 'panzer'

FEATURES = ["degree", "clustering_coefficient", "ego_net_edges"]

def say(*lst):
  print(*lst, end="")
  sys.stdout.flush()

def list_files(folder):
  """
  List all files in a folder
  :param folder: Name of the folder
  :return: list of complete file names in folder
  """
  return ["%s/%s"%(folder, f) for f in os.listdir(folder) if f.endswith(".txt")]

def make_graph(file_name):
  """
  Make graph from a file
  :param file_name:
  :return:
  """
  with open(file_name, 'r') as f:
    lines = f.readlines()
    node_count, edge_count = map(int, lines[0].strip().split())
    edges = [map(int, line.strip().split()) for line in lines[1:]]
    graph = Graph()
    graph.add_vertices(node_count)
    graph.add_edges(edges)
  for vertex in graph.vs:
    assign_attributes(vertex, graph)
  return graph


def assign_attributes(vertex, graph):
  """
  Assign Attributes for the vertex
  :param vertex: Vertex to be assigned attributes
  :param graph: Instance of graph to which the vertex belongs
  """
  neighbors = graph.neighbors(vertex.index)
  ego_net = graph.subgraph([vertex.index]+neighbors)
  vertex["degree"] = vertex.degree()
  cc = graph.transitivity_local_undirected([vertex.index])[0]
  vertex["clustering_coefficient"] = 0 if np.isnan(cc) else cc
  vertex["ego_net_edges"] = len(ego_net.es)


def get_feature_vector(graphs, vertex_id, feature):
  return [graph.vs[vertex_id][feature] for graph in graphs]

def pearson_rho(x_vector, y_vector):
  val, _ = pearsonr(x_vector, y_vector)
  return 0 if np.isnan(val) else val

def get_principal_eigen_vector(matrix):
  _, v = la.eig(matrix)
  return v[0]

def construct_correlation_matrix(all_graphs, feature, start, window=7):
  graphs = all_graphs[start:start+window]
  vertices = range(len(graphs[0].vs))
  matrix = []
  for x in vertices:
    x_vector = get_feature_vector(graphs, x, feature)
    covariance_vector = []
    for y in vertices:
      y_vector = get_feature_vector(graphs, y, feature)
      covariance_vector.append(pearson_rho(x_vector, y_vector))
    matrix.append(covariance_vector)
  return matrix

def vector_average(vectors):
  total = vectors[0]
  count = 1
  for vector in vectors[1:]:
    total = total + vector
    count += 1
  return total / count

def construct_correlation_matrices(all_graphs, window=7):
  feature_info = {}
  for feature in FEATURES:
    matrices = []
    eigens = []
    for start in range(len(all_graphs)-window):
      say(".")
      matrix = construct_correlation_matrix(all_graphs, feature, start, window)
      matrices.append(matrix)
      eigens.append(get_principal_eigen_vector(matrix))
    feature_info[feature] = {
      "matrices" : matrices,
      "eigens" : eigens
    }
    print("%s completed"%feature)
  return feature_info

def compute_eigen_behaviour(feature_info, window=7):
  eigen_behaviours = {}
  for feature in FEATURES:
    eigens =  feature_info[feature]["eigens"]
    eigen_behaviour = []
    for start in range(len(eigens)-window):
      u_t = eigens[start+window]
      r_t1 = vector_average(eigens[start:start+window])
      eigen_behaviour.append(round(np.dot(u_t, r_t1).real, 2))
    eigen_behaviours[feature] = eigen_behaviour
  return eigen_behaviours

def save_eigen_behaviours(eigen_behaviours, file_name):
  lines = [" ".join(FEATURES)+"\n"]
  vals = []
  for feature in FEATURES:
    vals.append(eigen_behaviours[feature])
  vals = zip(*vals)
  for line in vals:
    lines.append(" ".join(map(str, line))+"\n")
  with open(file_name, 'w') as f:
    f.writelines(lines)

def plot_eigen_behaviours(eigen_behaviours, file_name, window = 7):
  xs = range(window,len(eigen_behaviours.values()[0])+window)
  colors = ["r", "g", "b"]
  f, axis_arr = plt.subplots(3, sharex=True)
  for i, feature in enumerate(FEATURES):
    ys = eigen_behaviours[feature]
    axis_arr[i].plot(xs, ys, "%s-"%colors[i])
    axis_arr[i].set_ylabel("Z Score")
  plt.xlabel("Time")
  plt.xlim(0, xs[-1]+2)
  plt.savefig(file_name)
  plt.clf()



def _main(folder):
  graphs = []
  for f in list_files(folder):
    graphs.append(make_graph(f))
  print("Graphs Processed")
  feature_info = construct_correlation_matrices(graphs)
  eigen_behaviours = compute_eigen_behaviour(feature_info)
  dataset = folder.split("/")[-1]
  ts_file_name = "%s_time_series.txt"%dataset
  ts_png_name = "%s_time_series.png"%dataset
  save_eigen_behaviours(eigen_behaviours, ts_file_name)
  plot_eigen_behaviours(eigen_behaviours, ts_png_name)


if __name__ == "__main__":
  args = sys.argv
  if len(args) != 2:
    print("USE THE COMMAND : python anomaly.py <data folder>")
    exit()
  folder_name = args[1]
  _main(folder_name)