# Running the python script on a local machine

## Prerequisite

1. [Install](https://sparkbyexamples.com/pyspark/how-to-install-pyspark-on-mac/) [Apache-Spark](https://spark.apache.org/). Avoid installing java as  OpenJDK version 11. [Install](https://www.java.com/en/download/help/download_options.html) java by using this link. 

2. You can use use any good code editor but I personally prefered [jupitar-lab](https://jupyter.org/install) to run this script. 
 
## Running the script 

1. Create a folder named outputFolder in the python-pyspark folder. 
2. Right click on the folder name to copy the file path. 
3. Open the terminal and cd into the python-pyspark folder and type the below command remember to 
   replace the --output_uri link "/uri/output/folder/to/store/results"  with your outputFolder path.

```shellcommand
spark-submit analysis.py --data_source_1 x_list.txt --data_source_2 y_list.txt --output_uri /uri/output/Folder/to/store/results

```
4. To execute the script in jupiter-lab or note book, create a new python 3 note book and type the below command by replacing the --output_uri link,  "/uri/output/folder/to/store/results" with your outputFolder path.

```shellcommand

!spark-submit analysis.py --data_source_1 x_list.txt --data_source_2 y_list.txt --output_uri /uri/output/folder/to/store/results

```

Terminal output 

```shellcommand

+----+-------+-------+
|ID_x|value_x|value_y|
+----+-------+-------+
|  ID|   Word|   droW|
|   A|  Hello|  olleH|
|   B|  World|  dlroW|
|   C|    How|    woH|
|   D|     Do|     oD|
|   E|    You|    uoY|
|   F|     Do|     oD|
|   G|      ?|      ?|
+----+-------+-------+

```

