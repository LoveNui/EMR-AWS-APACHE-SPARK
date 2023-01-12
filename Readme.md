
# **Executing an existing python script on aws cloud for data analytics.**

 
## **Use Case**
 
Our use case focuses on a data scientist who just finished the attached Python script, with a view to run it on very large files (e.g. billions of rows).The data scientist needed help to package it up into a pipeline to run at scale on the cloud.

```python

import sys
import pandas as pd
import numpy as np

"""
Merge 2 files into 1

Usage:
python3 ./analysis.py x_list.txt y_list.txt
"""

def main():
    x = pd.read_csv(sys.argv[1], sep="\t")
    y = pd.read_csv(sys.argv[2], sep="\t")
    print(x)

    res = pd.DataFrame.from_records(
        [
            np.concatenate((x_row, y_row), axis=None)
            for x_index, x_row in x.iterrows()
            for y_index, y_row in y.iterrows()
        ],
        columns=["ID_x", "value_x","ID_y","value_y"],
    )

    print(res[res["ID_x"] == res["ID_y"]].drop(columns="ID_y"))


if __name__ == "__main__":
    main()


```
 
 
## **Possible Solutions** 

For this Amazon AWS cloud infrastructure is used. 

## **Solution 1: Data processing with Aws lamda function and uploading the data in amazon S3 bucket.** 
 
The main parts of this architecture we discuss are (Figure 1):
 
1. A data source [amazon S3](https://aws.amazon.com/s3/) is where data files are uploaded.
 
2. A data processing solution an [aws lambda function](https://aws.amazon.com/lambda/) where the above python script is exxecuted. 
 
3. A data storage such as an [amazon S3](https://aws.amazon.com/s3/) where the results of the data processing can be stored.
 
4. Application integration module an [amazon event notification](https://aws.amazon.com/s3/)can monitor events happen in the S3 bucket and take actions based on those events to run a lambda function with the python script and send a email to the data scientist when a file is uploaded to s3 data source through [amazon SNS](https://aws.amazon.com/sns/) and when the results are uploaded to the s3 data storage.
 
5. [Amazon cloudWatch logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) to monitor, store, and access your log files from AWS lambda function and s3.
  
![architecture1](images/aws-s3-lamda-architecture.png)
Figure 1. Data pipeline for running a python script on AWS lamda function.

### **Advantanges**

* No servers to manage 
* Continous scaling 
* Millisecond metering


### **Disdvantages**

* The maximum time a lambda function can run is 15 minutes.
* Lambda function may not be able to handle big file systems like the dataset mentioned in this use case with
  billions of rows.
* When its comes to big data lambda functions may not be that cost effective. 

### **Conclusion** 

So solution 2 may not be ideal for this usecase which take us to solution 2. 


## **Solution 2: Data processing in [amazon EMR](https://aws.amazon.com/emr/) with spark and hadoop and uploading the data in [amazon S3 bucket](https://aws.amazon.com/s3/).**


The main parts of this architecture we discuss are (Figure 2):

![architecture2](images/Architecture-EMR-S3.png)
Figure 2. Data pipeline for running a python script on AWS EMR

1. A data source [amazon S3](https://aws.amazon.com/s3/) is where data files are uploaded.

2. A data processing solution an [AWS EMR](https://aws.amazon.com/emr/) where the above python script is exxecuted. [AWS EMR](https://aws.amazon.com/emr/) (Elastic Map reduce) is a big data on demand server. It is preconfigured with spark hadoop etc. It has a master node and ec2 intances as worker nodes. We can scale up the ec2 instances as our requirements. 
 
3. [Amazon cloudWatch logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) to monitor, store, and access your log files from AWS lambda function and s3.








