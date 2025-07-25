# 🧠 AWS Glue Data Lake Project for Health & Fitness Tracking
This repository contains my solution for a serverless data lake project using AWS Glue, Athena, and S3. The project simulates real-world data engineering tasks by ingesting JSON data from multiple sources, performing ETL transformations, filtering PII, and organizing the data into Landing, Trusted, and Curated zones.

🚀 Project Overview:<br>

This project demonstrates a modern data lake architecture using AWS Glue to process and transform raw JSON data stored in S3 into clean, queryable formats accessible through Amazon Athena. The data represents customers, accelerometer sensor readings, and step trainer devices.

✅ Project Pipeline <br>

🧾 Data Sources (Landing Zone): <br>
- Raw JSON files are ingested into Amazon S3 from: <br>
    - Website Form: customer_landing <br>
    - Mobile App: accelerometer_landing <br>
    - IoT Device: step_trainer_landing
    
🛠 Glue Jobs
1. Landing to Trusted Zone
- Customer Landing to Trusted.py
    - Goal: Sanitize customer data to retain only users who agreed to share data for research (Filters out records with missing shareWithResearchAsOfDate).
    - Logic: Drop any customer record missing shareWithResearchAsOfDate.
    - Writes cleaned customer data to customer_trusted.

- Accelerometer Landing to Trusted.py
    - Goal: Retain only accelerometer readings from users who consented to share data.
    - Logic: Inner join accelerometer_landing with customer_trusted on email.
    - Outputs only accelerometer fields into accelerometer_trusted.

- Step Trainer Landing to Trusted.py
    - Goal: Store Step Trainer IoT records only for customers who have both accelerometer data and have agreed to share their data.
    - Logic: Inner join step_trainer_landing with customer_curated on serialNumber.

2. Trusted to Curated Zone
- Customer Trusted to Curated.py
    - Goal: Identify customers who have both accelerometer data and have agreed to share their data.
    - Logic: Join customer_trusted and accelerometer_trusted on email, keeping only customer fields.

- Machine Learning Curated.py
    - Goal: Aggregate sensor data for machine learning analysis.
    - Logic: Join step_trainer_trusted with accelerometer_trusted on sensorReadingTime.

🛠 Glue Jobs Summary <br>
|Glue Job | Description|
|:---:|:---:|
| Customer Landing to Trusted.py | Filters customers with non-null shareWithResearchAsOfDate.|
| Accelerometer Landing to Trusted.py | Joins raw accelerometer data with customer_trusted using email.|
| Step Trainer Landing to Trusted.py | Filters IoT records for customers in customers_curated.|
| Customer Trusted to Curated.py | Joins customer_trusted with accelerometer_trusted to create customers_curated.|
| achine Learning Curated.py | Joins step_trainer_trusted with accelerometer_trusted on sensorReadingTime.|

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
