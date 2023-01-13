
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

## **Solution 1: Data processing with Aws lamda function and data in amazon S3 bucket.** 
 
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

Though AWS lamda function has many advantages and cost savings its is not an ideal solution for this usecase, which takes us to solution 2.


## **Solution 2: Data processing in [amazon EMR](https://aws.amazon.com/emr/) with [apache spark](https://aws.amazon.com/big-data/what-is-spark/) with data in [amazon S3 bucket](https://aws.amazon.com/s3/).**

Apache Spark is an open-source, distributed processing system used for big data workloads. It utilizes in-memory caching, and optimized query execution for fast analytic queries against data of any size. Amazon EMR is the industry-leading cloud big data platform for data processing, interactive analysis, and machine learning using open source frameworks such as Apache Spark. 

The main parts of this architecture we discuss are (Figure 2):

![architecture2](images/Architecture-EMR-S3.png)
Figure 2. Data pipeline for running a python script on AWS EMR

1. A data source [amazon S3](https://aws.amazon.com/s3/) is where data files are uploaded.

2. A data processing solution an [AWS EMR](https://aws.amazon.com/emr/) where the above python script is exxecuted. [AWS EMR](https://aws.amazon.com/emr/) (Elastic Map reduce) is a big data on demand server. It is preconfigured with spark hadoop etc. It has a master node and ec2 intances as worker nodes. We can scale up the ec2 instances as our requirements. 
 
3. [Amazon cloudWatch logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) to monitor, store, and access your log files from AWS lambda function and s3.



### **Python script modification** 

The above python script is written using pandas library and pandas has a disadvantage pandas run operations on a single machine. In this solution since we are using Apache Spark in an EMR cluster with multiple machines so we need to rewrite the python script with PySpark. PySpark is an ideal fit for our usecase with big data as it could processes operations many times(100x) faster than Pandas.

```python

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType


def main():
    """
    Merge 2 files into 1

    Usage:
    spark-submit analysis.py
    """
    spark = SparkSession.builder.appName("Merge-two-files").getOrCreate()

    S3_BUCKET_DATA_SOURCE_1 = 's3://DOC-EXAMPLE-BUCKET/DATA_SOURCE/x_list.txt'
    S3_BUCKET_DATA_SOURCE_2 = 's3://DOC-EXAMPLE-BUCKET/DATA_SOURCE/y_list.txt'
    S3_BUCKET_DATA_OUTPUT = 's3://DOC-EXAMPLE-BUCKET/DATA_OUTPUT'

    x_schema = StructType([
        StructField("ID_x", StringType(), True),
        StructField("value_x", StringType(), True)])

    y_schema = StructType([
        StructField("ID_y", StringType(), True),
        StructField("value_y", StringType(), True)])

    x = spark.read.csv(S3_BUCKET_DATA_SOURCE_1, sep='\t',
                       header=False, schema=x_schema)
    y = spark.read.csv(S3_BUCKET_DATA_SOURCE_2, sep='\t',
                       header=False, schema=y_schema)
    res = x.join(y, x.ID_x == y.ID_y, how="left")
    res1 = res.drop(res.ID_y)
    res1.show()
    
    res1.write.parquet(S3_BUCKET_DATA_OUTPUT, mode="overwrite")
    


if __name__ == "__main__":
    main()


```

### **Advantanges**
* Cost savings especially if we use spot instances for big data. 
* Code Deployment is easy. 
* Integration with other AWS services
* Scalability and flexibility
* Reliability
* Security
* Monitoring
* No data file size limit and no maximum run time like lamda function. 



### ***Disadvantages**
* Its ideal only for big data.
* Manually deploy and start the EMR clusters. 
* We can set the ec2 intances termination periods but if our task execution completes before the termination 
  period we will have to manually terminate the instances to save cost.
 


### **Conclusion** 

AWS EMR has many advantages when it comes to big data processing as it uses apache spark with distributed system. Its has some disavantages also as its not completely severless and we will have manually start and stop the clusters. AWS EMR is a good solution for our use case. 

### [**Click here for an EMR SOP**](/EMR-SOP.md).

## **Solution 3: Data processing in [amazon EMR serverless](https://aws.amazon.com/emr/serverless/) with [apache spark](https://aws.amazon.com/big-data/what-is-spark/) with data in [amazon S3 bucket](https://aws.amazon.com/s3/).**


## How would you set up the company’s cloud account to run pipelines securely and robustly?


