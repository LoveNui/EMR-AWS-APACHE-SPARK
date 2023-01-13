from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType

def main():
    """
    Merge 2 files into 1

    Usage:
    spark-submit analysis.py
    """
    spark=SparkSession.builder.appName("devops-tech-test").getOrCreate()

    S3_BUCKET_DATA_SOURCE_1 = 's3://devops-tech-test/data-source/x_list.txt'
    S3_BUCKET_DATA_SOURCE_2 = 's3://devops-tech-test/data-source/y_list.txt'
    S3_BUCKET_DATA_OUTPUT = 's3://devops-tech-test/data-output'
    
    x_schema = StructType([
    StructField("ID_x", StringType(), True),
    StructField("value_x", StringType(), True)])
    
    y_schema = StructType([
    StructField("ID_y", StringType(), True),
    StructField("value_y", StringType(), True)])
    
    x = spark.read.csv(S3_BUCKET_DATA_SOURCE_1, sep='\t',header=False,schema=x_schema)
    y = spark.read.csv(S3_BUCKET_DATA_SOURCE_2, sep='\t', header=False, schema=y_schema)
    res = x.join(y, x.ID_x == y.ID_y, how= "left")
    res1 = res.drop(res.ID_y)
    res1.write.parquet(S3_BUCKET_DATA_OUTPUT,mode="overwrite")
    res1.show()

if __name__ == "__main__":
    main()
