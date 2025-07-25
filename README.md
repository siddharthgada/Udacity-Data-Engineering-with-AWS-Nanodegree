# Data Engineering

## Data Modeling Course

### Skills Acquired:
- Relational data modeling with PostgreSQL
- How to create tables and insert data into PostgreSQL
- NoSQL data modeling with Apache Cassandra
- How to create tables and insert data into Apache Cassandra
- The process of database normalization and the normal forms.
- Denormalization and when it should be used.
- Fact vs dimension tables as a concept and how to apply that to our data modeling
- How the star and snowflake schemas use the concepts of fact and dimension tables to make getting value out of the data easier.
- Basics of Distributed Database Design

Proficiencies used: PostgreSQL, Apache Cassandra(CQL), Normalization, Denormalization

### Project 1: NoSQL Databases - Data Modeling with Apache Cassandra
Developed a NoSQL database using Apache Cassandra to model user activity data for a music streaming app. <br>

Skills include:
- Created a NoSQL database using Apache Cassandra
- Developed denormalized tables optimized for a specific set of queries and business needs

Proficiencies used: Python, Apache Cassandra(CQL), Denormalization

## Cloud Data Warehouse Course

### Skills Acquired:
- Practiced ETL steps from a 3NF database to a Star Schema
- Practiced slicing, dicing, Roll Up and Drill Down operations with OLAP cubes
- Using ETL and ELT techniques
- Using Relational and NoSQL databases in the cloud
- Creating an IAM role and user, security group, S3 bucket, PostgreSQL Database
- Launching a Redshift Cluster
- How to ETL with Redshift
- How to ingest data into Redshift using S3 buckets
- Parallel ETL
- Optimizing Table Design using Distribution Styles

Proficiencies used: SQL, PostgreSQL, AWS Redshift, AWS EC2, AWS S3, AWS IAM, Normalization, Denormalization

### Project 2: Data Warehouse
Built a cloud-based ETL pipeline and data warehouse for Sparkify, a fictional music streaming company. The goal was to migrate raw JSON log and song metadata from S3 into AWS Redshift and model the data using a star schema for analytical queries on user listening behavior. <br>

Skills include:
- Designed fact (songplays) and dimension tables (users, songs, artists, time) based on the star schema.
- Optimized for query performance using appropriate distribution and sort keys.
- Developed denormalized tables optimized for a specific set of queries and business needs
- Extracted raw JSON data from S3.
- Loaded data into staging tables using Redshift COPY command.
- Transformed and inserted cleaned data into final tables using Python and SQL.

Proficiencies used: AWS Redshift, AWS S3, ETL, SQL, Star Schema, Python, psycopg2

## Spark And Data Lakes Course

### Skills Acquired:
- Big Data Foundations: Gained understanding of Hadoop, MapReduce, Apache Spark, and the principles of data lakes and lakehouse architecture.
- Spark Data Processing: Practiced data wrangling using PySpark DataFrames and Spark SQL for scalable data transformations.
- AWS Glue & Cloud Integration:
  - Configured IAM roles, VPC endpoints, and permissions for secure Glue access to S3.
  - Built and orchestrated Spark-based ETL pipelines using AWS Glue Studio.
- Data Lakehouse Architecture:
  - Implemented multi-zone lakehouse structure (Landing, Trusted, Curated).
  - Filtered and transformed PII data according to zone-based access control.
  - Joined batch and streaming datasets using Spark for machine learning readiness.

Proficiencies used: Apache Spark, PySpark, Spark SQL, AWS Glue, S3, IAM, VPC, Data Lakehouse

### Project 3: STEDI Human Balance Analytics
Built a serverless data lake architecture to process health and fitness telemetry data using AWS Glue and PySpark. Implemented multi-stage ETL pipelines to ingest, clean, and transform raw JSON data into queryable tables for machine learning analysis.

Skills include:
- Designed multi-zone architecture (Landing → Trusted → Curated) on S3 and Glue.
- Filtered PII and retained only customers who consented to data sharing.
- Joined sensor and IoT data streams on timestamp for ML readiness.
- Created Sprak jobs with Glue Studio to manage schema evolution and data manipulation.
- Queried data using Amazon Athena.

Proficiencies used: AWS Glue Studio, PySpark, Amazon S3, Athena, ETL, SQL, IAM, VPC

  ## 👤 Author

**Siddharth Gada**  
📧 Email: gadasiddharth@gmail.com <br>
🔗 LinkedIn: https://www.linkedin.com/in/siddharthgada/
