# Graph Data Mining

This project is to implement the alogrithm discussed in Paper 1: WebGraph Similarity for Anomaly Detection.

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
unzip anomaly.zip
cd anomaly
```

Once the path is under `anomaly`, please run the command in following format.

```
python3 anomaly.py <path/to/file/file>
```

For example, if we would like to run the `voices` dataset, please run the command as following:

```
python3 anomaly.py voices
```

After the program complete, the results will be saved on the current directory, the program should run within 1 min except `autonomous` dataset which requires 10 mins to 20 mins to complete.
