# 🧠 AWS Glue Data Lake Project for Health & Fitness Tracking
This repository contains my solution for a serverless data lake project using AWS Glue, Athena, and S3. The project simulates real-world data engineering tasks by ingesting JSON data from multiple sources, performing ETL transformations, filtering PII, and organizing the data into Landing, Trusted, and Curated zones.

🚀 Project Overview:<br>

This project demonstrates a modern data lake architecture using AWS Glue to process and transform raw JSON data stored in S3 into clean, queryable formats accessible through Amazon Athena. The data represents customers, accelerometer sensor readings, and step trainer devices.

✅ Project Pipeline <br>
🧾 Data Sources (Landing Zone) <br>
- S3 JSON files for: <br>
    - customer_landing <br>
    - accelerometer_landing <br>
    - step_trainer_landing
    
2. ETL Pipeline Development
  - Implemented logic in Part I of the notebook to iterate through raw event files (event_datafile_new.csv) and processed them into a new, denormalized CSV format.
  - Edited Part II of the notebook to include Cassandra CREATE and INSERT statements that will load the processed records into the relevant tables in the data model.
  - Tested the ETL pipeline by running SELECT statements to verify the data load.

3. Running Queries
  - Executed the queries provided in the template against the newly created tables.
  - Ensured that queries return the expected results and are optimized for performance, especially with large datasets.

🔍 Key Learning Outcomes: <br>
📌 Designing NoSQL Databases <br>
  - Learned how to design a Cassandra database schema for event-based data, ensuring efficient querying and data storage in a distributed     database environment. <br>
📌 Data Processing and ETL Pipelines<br>
  - Gained experience in ETL processes by writing Python code to process raw event data into a structured format and load it into Apache      Cassandra. <br>
📌 Apache Cassandra Syntax<br>
  - Familiarized with Cassandra Query Language (CQL) for creating and managing keyspaces, tables, and inserting records into a      
    distributed NoSQL database. <br>
📌 Performance Optimization <br>
  - Learned how to design data models that allow for quick query performance, using partition keys, clustering columns, and understanding     Cassandra's limitations and optimizations. <br>

📂 Project Deliverables:<br>
1. Data Loading and ETL Pipeline
  - Processed raw CSV files into a denormalized format.
  - Python Code: Includes ETL pipeline code to process and load data into Cassandra.
2. SQL Queries
  - Written and tested SQL queries to answer specific business questions from the event data.

📊 Technologies & Tools Used: <br>
1. Apache Cassandra: NoSQL database to store and retrieve structured event data.
2. Python (Pandas): Used for processing the event data and handling the ETL pipeline.
3. Cassandra Query Language (CQL): Used for creating tables, inserting data, and querying the database.
