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
unzip whu24.zip
cd GDM_Project2
```

Once the path is under `GDM_Project2`, please run the command in following format.

```
python3 anomaly.py <path/to/file/file>
```

For example, if we would like to run the `voices` dataset, please run the command as following:

```
python3 anomaly.py voices
```

After the program complete, the final communiites will be store in `result/output.txt`, the program should run 3 mins to 10 mins depends on the graph size.
