# Graph Data Mining

This project 4 is to implement the alogrithm discussed in Paper 1, WebGraph Similarity for Anomaly Detection.

## Environment to test the script
This project has been tested on `CSC591_ADBI_v3` VCL environment.

## Packages requirment
Please ensure the `networkx` to be installed beforehand, or run the following command to install:
```
pip3 install networkx
```
If the installtion failed from the command above, please download from website and following the instructioins on the website to install.
[https://pypi.org/project/networkx/#files](https://pypi.org/project/networkx/#files)

## How to run the script
After download the zip, first unzip the zip file and get into the folder.
```
unzip GDM_Project2.zip
cd GDM_Project2
```
Once the path is under `GDM_Project2`, please run the command in following format. 
```
python3 main.py <path/to/file/file>
```
For example, if we would like to run the `amazon.graph.small`, please run the command as following:
```
python3 main.py ./datasets/amazon/amazon.graph.small 
```
After the program complete, the final communiites will be store in `result/output.txt`, the program should run 3 mins to 10 mins depends on the graph size.

Note that if `output.txt` will be overwrited if re-run the prorgam.
The output file will be in the format as below:
```
0 1
2 3 6 7 119 119
35 366 988 23 98 112 
```
Each line present the nodes with same community and, for example, the second community contains 6 nodes.


# Description: The code uses the following Libraries.
# numpy, pandas, igraph
# Installation Instructions: 
# Igraph : pip install python-igraph(Please refer to the official documentations for more platform specific details.)
# The data folder must be present in the directory where this file resides.
# The program generates the Time Series of the similarities between the graphs over time for one dataset at a time.
# Saves the graph in the file called "<dataset_name>_time_series.pdf"
# Saves the series in file called "<dataset_name>_time_series.txt"
# Please run the code as python anomaly.py <dataset_folder> from the directory it resides.
# Sample usage : python anomaly.py datasets/datasets/voices/
# The parameter b for hashing is kept as 64 as a default. Can be increased for more accuracy at the cost of computing efficiency.

# Estimated Running times:
# voices : 0.47 seconds.
# enron : 9.43 seconds.
# p2p : 52 seconds.
# autonomous : 648 seconds.