#!/usr/bin/env python
# coding: utf-8

# # Data Wrangling with Spark SQL Quiz
# 
# This code uses the same dataset and most of the same questions from the earlier code using dataframes. For this scropt, however, use Spark SQL instead of Spark Data Frames.



# TODOS: 
# 1) import any other libraries you might need
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import desc
from pyspark.sql.window import Window
import datetime

# 2) instantiate a Spark session 
spark = SparkSession \
    .builder \
    .appName("Data Wrangling With Spark SQL") \
    .getOrCreate()

# 3) read in the data set located at the path "data/sparkify_log_small.json"
path = "/workspace/home/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/lesson-2-spark-essentials/exercises/data/sparkify_log_small.json"
user_log_df = spark.read.json(path)
# 4) create a view to use with your SQL queries
user_log_df.createOrReplaceTempView("user_logs_table")
# 5) write code to answer the quiz questions 


# # Question 1
# 
# Which page did user id ""(empty string) NOT visit?

# TODO: write your code to answer question 1

# Show all the unique values in the "page" column from the entire dataset
spark.sql('''
    SELECT DISTINCT page AS blank
    FROM user_logs_table
    WHERE userID != ""
        ''').show()

# Show all the unique values in the "page" column from rows that have empty "userID" columns
spark.sql('''
    SELECT DISTINCT page AS blank
    FROM user_logs_table
    WHERE userID = ""
        ''').show()

# # Question 2
# 
# How many female users do we have in the data set?

# TODO: write your code to answer question 3
spark.sql('''
    SELECT COUNT(DISTINCT userID) as female_count
    FROM user_logs_table
    where gender = "F"
        ''').show()

# # Question 3
# 
# How many songs were played from the most played artist?

# TODO: write your code to answer question 4
spark.sql('''
    SELECT MAX(cnt) as count
    FROM (SELECT Artist, COUNT(userID) as cnt
            FROM user_logs_table
            WHERE page = "NextSong"
            GROUP BY Artist)
        ''').show()
# # Question 4 (challenge)
# 
# How many songs do users listen to on average between visiting our home page? Please round your answer to the closest integer.

# TODO: write your code to answer question 5
query = '''
    WITH cusum AS (
        SELECT userID, page, ts,
            CASE WHEN page = 'Home' THEN 1 ELSE 0 END AS homevisit,
            SUM(CASE WHEN page = 'Home' THEN 1 ELSE 0 END) OVER (
                PARTITION BY userID
                ORDER BY ts DESC
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS period
        FROM user_logs_table
        WHERE page IN ('NextSong', 'Home')
                    )
    SELECT ROUND(AVG(song_count)) AS average_songs
    FROM (
        SELECT userID, period, COUNT(period) AS song_count
        FROM cusum
        WHERE page = 'NextSong'
        GROUP BY userID, period
            )
        '''

result = spark.sql(query).show()
