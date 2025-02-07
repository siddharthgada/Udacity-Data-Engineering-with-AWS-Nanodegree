# Apache Cassandra Data Modeling and ETL Pipeline Project
This repository contains my solution for the Apache Cassandra Data Modeling and ETL Pipeline Project, which focuses on processing event data, 
creating a NoSQL data model, and loading it into Apache Cassandra. The project template includes steps for designing tables, processing data 
and executing queries.

🚀 Project Overview<br>
This project involves the following key components:

1. Data Modeling: Designing a NoSQL data model to structure event data in a way that allows for efficient query processing in Apache Cassandra.
2. ETL Pipeline: Implementing a pipeline to process raw event data into a denormalized format and load it into Cassandra.
3. Query Execution: Ensuring the design is optimized to run a set of predetermined business queries efficiently.

✅ Project Steps
1. Modeling the Apache Cassandra Database
  - Designed the tables needed to answer the queries outlined in the project template.
  - Wrote CREATE KEYSPACE and SET KEYSPACE statements to set up the appropriate keyspace.
  - Developed CREATE TABLE statements for each query, considering the necessary data structure for efficient querying.
  - Included IF NOT EXISTS clauses in the CREATE statements to ensure that tables are only created if they do not already exist.
  - Optionally, included DROP TABLE statements to allow for resetting the database for testing.
    
2. ETL Pipeline Development
  - Implemented logic in Part I of the notebook to iterate through raw event files (event_datafile_new.csv) and processed them into a new, denormalized CSV format.
  - Edited Part II of the notebook to include Cassandra CREATE and INSERT statements that will load the processed records into the relevant tables in the data model.
  - Tested the ETL pipeline by running SELECT statements to verify the data load.

3. Running Queries
  - Executed the queries provided in the template against the newly created tables.
  - Ensured that queries return the expected results and are optimized for performance, especially with large datasets.

🔍 Key Learning Outcomes<br>
📌 Designing NoSQL Databases <br>
  - Learned how to design a Cassandra database schema for event-based data, ensuring efficient querying and data storage in a distributed database environment.

📌 Data Processing and ETL Pipelines<br>
  - Gained experience in ETL processes by writing Python code to process raw event data into a structured format and load it into Apache Cassandra.

📌 Apache Cassandra Syntax<br>
  - Familiarized with Cassandra Query Language (CQL) for creating and managing keyspaces, tables, and inserting records into a distributed NoSQL database.
  
📌 Performance Optimization<br>
  - Learned how to design data models that allow for quick query performance, using partition keys, clustering columns, and understanding Cassandra's limitations and optimizations.

📂 Project Deliverables<br>
1. Data Loading and ETL Pipeline
  - Processed raw CSV files into a denormalized format.
  - Python Code: Includes ETL pipeline code to process and load data into Cassandra.
2. SQL Queries
  - Written and tested SQL queries to answer specific business questions from the event data.
3. Final Reports
  - Results from running the queries and any issues encountered.

📊 Technologies & Tools Used <br>
1. Apache Cassandra: NoSQL database to store and retrieve structured event data.
2. Python (Pandas): Used for processing the event data and handling the ETL pipeline.
3. Cassandra Query Language (CQL): Used for creating tables, inserting data, and querying the database.
