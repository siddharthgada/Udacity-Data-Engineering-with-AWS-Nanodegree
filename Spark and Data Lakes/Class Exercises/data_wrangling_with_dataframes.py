# # Data Wrangling with DataFrames Coding Quiz

from pyspark.sql import SparkSession

# TODOS: 
# 1) import any other libraries you might need
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import desc
from pyspark.sql.window import Window

import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 2) instantiate a Spark session 
spark = SparkSession \
    .builder \
    .appName("Data Wrangling Quiz") \
    .getOrCreate()
# 3) read in the data set located at the path "../../data/sparkify_log_small.json"
path = "/workspace/home/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/lesson-2-spark-essentials/exercises/data/sparkify_log_small.json"
user_log_df = spark.read.json(path)
# 4) write code to answer the quiz questions 


# # Question 1
# 
# Which page did user id "" (empty string) NOT visit?

# TODO: write your code to answer question 1
user_log_2_df = user_log_df.filter(user_log_df["userId"] == "")
user_log_2_df.show()

# Show all the unique values in the "page" column from the entire dataset
user_log_df.select("page").distinct().show()

# Show all the unique values in the "page" column from rows that have empty "userID" columns
user_log_2_df.select("page").distinct().show()

# # Question 2 - Reflect
# 
# What type of user does the empty string user id most likely refer to?

# Looks like a new user or someone who is getting to the know the app before 
# using it


# TODO: use this space to explore the behavior of the user with an empty string
user_log_2_df.describe().show()


# # Question 3
# 
# How many female users do we have in the data set?


# TODO: write your code to answer question 3
user_log_df.printSchema()

female_users_df = user_log_df.select("userID", "gender").dropDuplicates()
print(female_users_df.select("gender") \
    .where(female_users_df.gender == "F") \
    .count())

# # Question 4
# 
# How many songs were played from the most played artist?

# TODO: write your code to answer question 4
from pyspark.sql import functions as F

artist_df = user_log_df.filter(user_log_df.page == "NextSong")
artist_count_df = artist_df.select("artist").groupby("artist") \
    .agg(F.count("*").alias("artist_count"))

artist_count_df.agg(F.max("artist_count")).show()

# # Question 5 (challenge)
# 
# How many songs do users listen to on average between visiting our home page? Please round your answer to the closest integer.
# 
# 

# TODO: write your code to answer question 5
user_window = Window \
    .partitionBy("userID") \
    .orderBy(desc("ts")) \
    .rangeBetween(Window.unboundedPreceding, 0)

ishome = udf(lambda ishome : int(ishome == "Home"), IntegerType())

# Filtering only NextSong and Home pages, add 1 for each time they visit Home
# Adding a column called period which is a specific interval between Home visits
cusum = user_log_df.filter((user_log_df.page == "NextSong") | (user_log_df.page == "Home")) \
    .select("userID", "page", "ts") \
    .withColumn("homevisit", ishome("page")) \
    .withColumn("period", F.sum("homevisit") \
    .over(user_window)) 
    
# This will only show "Home" in the first several rows due to default sorting
cusum.show(300)


# See how many songs were listened to on average during each period
cusum.filter((cusum.page == "NextSong")) \
    .groupBy("userID", "period") \
    .agg(F.count("period").alias("song_count")) \
    .agg(F.ceil(F.avg("song_count"))) \
    .show()