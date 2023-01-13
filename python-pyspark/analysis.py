import argparse
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType

def merge_two_files(data_source_1,data_source_2,output_uri):
    """
    Merge 2 files into 1
    
    Usage 
    
    !spark-submit analysis.py --data_source_1 x_list.txt --data_source_2 y_list.txt --output_uri /uri/output/folder/to/store/results
    
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
    res1.write.option("header", "true").mode("overwrite").csv(output_uri)

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


