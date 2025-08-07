import pyspark
from pyspark import SparkConf
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Our first Python Spark SQL example") \
    .getOrCreate()

path = "/workspace/home/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/lesson-2-spark-essentials/exercises/data/sparkify_log_small.json"
user_log_df = spark.read.json(path)

# See how Spark inferred the schema from the JSON file
user_log_df.printSchema()
print(
    user_log_df.describe()
)

user_log_df.show(n=1)
print(
    user_log_df.take(5)
)

out_path = "/workspace/home/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/lesson-2-spark-essentials/exercises/data/sparkify_log_small.csv"
user_log_df.write.mode("overwrite").save(out_path, format="csv", header=True)

user_log_df_csv = spark.read.csv(out_path, header=True)

# See how Spark inferred the schema from the JSON file
user_log_df_csv.printSchema()

# Choose two records from the CSV file
print(
    user_log_df_csv.take(2)
) 

# Show the userID column for the first several rows
user_log_df_csv.select("userID").show()
