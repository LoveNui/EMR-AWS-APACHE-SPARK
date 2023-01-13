# Getting started with Amazon EMR

### Overview 

For detailed information on Amzon EMR please click [Amazon EMR documentation guide](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html). With Amazon EMR you can set up a cluster to process and analyze data with big data frameworks in just a few minutes.This tutorial shows you how to launch a sample cluster using Spark, and how to run a simple [PySpark script](/python-pyspark/analysis.py) stored in an Amazon S3 bucket. This python script is a PySpark version of the [Pandas script](/python-pandas/analysis.py. With modification to run the [x_list.txt](/python-pandas/x_list.txt) and [y_list.txt](/python-pandas/y_list.txt) data files from the S3 bucket and saving the results in s3 bucket again. 

We will be deploying the a python script which reads two files and join them into one file into an EMR cluster and we will saving the output in an s3 bucket. 


![EMR WORK FLOW](images/emr-workflow.png)
Figure 1: EMR work flow


### Step 1 : Creating an S3 bucket. (https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)

Using the S3 console
Sign in to the AWS Management Console with your username and password and open the Amazon S3 console at https://console.aws.amazon.com/s3/.

1. Choose Create bucket.The Create bucket wizard opens.

2. In Bucket name, enter a bucket name. After you create the bucket, you cannot change its name. For information about naming buckets, see [Bucket naming rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html).

4. In Region, choose the AWS Region such us EU west 1 or EU west 2.Choose a Region close to you to minimize latency and costs. 

5. Under Object Ownership ACLs disabled

6. In Bucket settings choose the Block Public Access settings.

7. Under Bucket Versioning, Enable.

8. Optional. To add a bucket tag, enter a Key and optionally a Value and choose Add Tag. 

9. Enable encryption

10. Choose Create bucket.

11. Click on the bucket name to go the bucket 

12. Click create folder and create two folders DATA_SOURCE and DATA_OUTPUT

13. Choose the DATA_SOURCE folder and choose Upload

14. Under Files and folders, choose Add files.

15. Choose a files  [x_list.txt](/DATA_SOURCE/x_list.txt) and [y_list.txt](/DATA_SOURCE/y_list.txt) to 
    upload, and then choose Open.

16. Choose Upload.

You've successfully uploaded an files to your bucket. Note: The maximum size of a file that you can upload by using the Amazon S3 console is 160 GB. To upload a file larger than 160 GB, use the AWS CLI, AWS SDK, or Amazon S3 REST API.

## Step 2: Prepare the above PySpark script for EMR

1. Copy the example code below into a new file in your editor of choice.

2. Replace the value of the variables S3_BUCKET_DATA_SOURCE_1, S3_BUCKET_DATA_SOURCE_2, S3_BUCKET_DATA_OUTPUT
   with values to the s3 bucket URI of these files and folders. You can a copy the URI link by choosing the files in the s3 bucket and clicking the copy URI button on the top. 

```python 

import argparse
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType

def merge_two_files(data_source_1,data_source_2,output_uri):
    """
    Merge 2 files into 1
    
    Usage 
    
    !spark-submit analysis.py --data_source_1 x_list.txt --data_source_2 y_list.txt --output_uri  fullpath/of/the/output/folder/to/save/result
    
    for example /Users/johnpaulbabu/Documents/pyspark/output
    """
    spark=SparkSession.builder.appName("merge-two-files").getOrCreate()
    
    x_schema = StructType([
    StructField("ID_x", StringType(), True),
    StructField("value_x", StringType(), True)])
    
    y_schema = StructType([
    StructField("ID_y", StringType(), True),
    StructField("value_y", StringType(), True)])
    
    if data_source_1 is not None:
      x = spark.read.csv(data_source_1, sep='\t',header=False,schema=x_schema)
    
    if data_source_2 is not None:
      y = spark.read.csv(data_source_2, sep='\t', header=False, schema=y_schema)
    
    res = x.join(y, x.ID_x == y.ID_y, how= "left")
    res1 = res.drop(res.ID_y)
    res1.show()
    res1.write.mode("overwrite").parquet(output_uri)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data_source_1', help="The URI for your input CSV data, like an S3 bucket location.")
    parser.add_argument(
        '--data_source_2', help="The URI for your input CSV data, like an S3 bucket location.")
    parser.add_argument(
        '--output_uri', help="The URI where output is saved, like an S3 bucket location.")
    args = parser.parse_args()
    

    merge_two_files(args.data_source_1, args.data_source_2,args.output_uri)

```

### Step 3: [Create EC2 key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html)

1. Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/.

2. In the navigation pane, under Network & Security, choose Key Pairs.

3. Choose Create key pair.

4. For Name, enter a descriptive name for the key pair. 

5. For Key pair type, choose either RSA or ED25519.

6. For Private key file format, choose the format pem. 

7. Choose Create key pair.

8. The private key file is automatically downloaded by your browser. The base file name is the name that you specified as the name of your key pair, and the file name with extension .pem. Save the private key file in a safe place.

9. Change the file permission of the key pair by chmod 400 and the file path where the key is stored. 

```shellcommand

chmod 400 filepath/key-pair-name.pem

```

### Step 4:Launch an Amazon EMR cluster


1. To launch an EMR cluster Sign in to the AWS Management Console, and open the Amazon EMR console at https://console.aws.amazon.com/emr/.

2. Under EMR on EC2 in the left navigation pane, choose Clusters, and then choose Create cluster.

3. In the Create Cluster page, note the default values for Release, Instance type, Number of instances, and Permissions. These fields automatically populate with values that work for general-purpose clusters.

4. In the Cluster name field, enter a unique cluster name to help you identify your cluster.

5. Under Applications, choose the Spark option to install Spark on your cluster.

6. Under Cluster logs, select the Publish cluster-specific logs to Amazon S3 check box. Replace the Amazon S3 location value with the Amazon S3 bucket you created, followed by /logs. For example, s3://DOC-EXAMPLE-BUCKET/logs. Adding /logs creates a new folder called 'logs' in your bucket, where Amazon EMR can copy the log files of your cluster.

7. Under Security configuration and permissions, choose your EC2 key pair. In the same section, select the Service role for Amazon EMR dropdown menu and choose EMR_DefaultRole. Then, select the IAM role for instance profile dropdown menu and choose EMR_EC2_DefaultRole.

8. Choose Create cluster to launch the cluster and open the cluster details page.

9. Find the cluster Status next to the cluster name. The status changes from Starting to Running to Waiting
   as Amazon EMR provisions the cluster. You may need to choose the refresh icon on the right or refresh your browser to see status updates.

### Step 5: Submit work to Amazon EMR



