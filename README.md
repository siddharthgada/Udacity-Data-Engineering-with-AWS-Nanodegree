# Data Engineering with AWS Nanodegree – Udacity

## 1. Data Modeling Course
**Skills Acquired**
- Relational data modeling with PostgreSQL
- Creating tables and inserting data into PostgreSQL
- NoSQL data modeling with Apache Cassandra
- Creating tables and inserting data into Apache Cassandra
- Database normalization and normal forms
- Denormalization and when to use it
- Fact vs. dimension tables and applying them in data modeling
- Star and snowflake schemas for easier data analytics
- Basics of distributed database design

**Proficiencies Used:** PostgreSQL, Apache Cassandra (CQL), Normalization, Denormalization

**Project 1: NoSQL Databases – Data Modeling with Apache Cassandra**
- Developed a NoSQL database using Apache Cassandra to model user activity data for a music streaming app.
- Designed and implemented denormalized tables optimized for specific business queries.
- Created CQL-based schemas and inserted query-ready datasets.

**Proficiencies Used:** Python, Apache Cassandra (CQL), Denormalization

---

## 2. Cloud Data Warehouse Course
**Skills Acquired**
- ETL from 3NF database to Star Schema
- OLAP cube operations (slice, dice, roll-up, drill-down)
- ETL and ELT techniques in cloud environments
- Relational and NoSQL databases in the cloud
- AWS setup: IAM roles, S3 buckets, security groups, Redshift clusters
- Redshift COPY command for bulk ingestion from S3
- Parallel ETL and table design optimization (distribution & sort keys)

**Proficiencies Used:** SQL, PostgreSQL, AWS Redshift, AWS EC2, AWS S3, AWS IAM, Normalization, Denormalization

**Project 2: Data Warehouse**
- Built a cloud-based ETL pipeline and data warehouse for Sparkify, a fictional music streaming company.
- Migrated raw JSON log and song data from S3 into AWS Redshift and modeled it using a star schema for analytical queries.
- Designed fact (songplays) and dimension tables (users, songs, artists, time) in a star schema.
- Optimized queries using distribution and sort keys.
- Extracted JSON data from S3 and staged it in Redshift.
- Transformed and loaded cleaned data into analytics tables using Python and SQL.

**Proficiencies Used:** AWS Redshift, AWS S3, ETL, SQL, Star Schema, Python, psycopg2

---

## 3. Spark and Data Lakes Course
**Skills Acquired**
- Big Data foundations: Hadoop, MapReduce, Apache Spark, data lakes, and lakehouse architecture
- Data wrangling with PySpark DataFrames and Spark SQL
- AWS Glue integration with IAM, VPC, and S3
- ETL pipeline orchestration in AWS Glue Studio
- Lakehouse architecture: Landing, Trusted, and Curated zones
- PII filtering and zone-based access control
- Batch and streaming data joins for ML readiness

**Proficiencies Used:** Apache Spark, PySpark, Spark SQL, AWS Glue, S3, IAM, VPC, Data Lakehouse

**Project 3: STEDI Human Balance Analytics**
- Built a serverless data lake architecture to process IoT sensor and customer balance data using AWS Glue and PySpark.
- Designed multi-zone architecture (Landing → Trusted → Curated)
- Filtered PII and kept only consented customers.
- Joined IoT telemetry and customer datasets on timestamps for ML readiness.
- Created Spark jobs with Glue Studio to manage schema evolution.
- Queried transformed datasets using Amazon Athena.

**Proficiencies Used:** AWS Glue Studio, PySpark, Amazon S3, Athena, ETL, SQL, IAM, VPC

---

## 4. Automated Data Pipelines Course
**Skills Acquired**
- Workflow orchestration with Apache Airflow
- Building modular, parameterized DAGs for ETL workflows
- Creating reusable custom Python operators for staging, fact loading, dimension loading, and data quality checks
- Automating ingestion from S3 to Amazon Redshift Serverless using COPY commands
- Implementing automated data validation checks to ensure reliability
- Supporting both append (incremental) and truncate (full refresh) load strategies
- Applying Airflow best practices: retries, backfills, task dependencies, and parameterization

**Proficiencies Used:** Apache Airflow, Python, Amazon S3, Amazon Redshift Serverless, AWS IAM, SQL, ETL, Data Quality Checks

**Project 4: Data Pipelines with Airflow**
- Built and deployed an automated ETL pipeline for Sparkify, orchestrating data ingestion from S3 to Redshift using Apache Airflow.
- Developed parameterized Airflow DAGs with task dependencies and scheduling.
- Created `StageToRedshiftOperator`, `LoadFactOperator`, `LoadDimensionOperator`, and `DataQualityOperator`.
- Supported both append and truncate load strategies for dimensions.
- Staged JSON data from S3 into Redshift staging tables.
- Transformed and loaded data into star schema fact and dimension tables.
- Configured Airflow connections and variables for dynamic runs.
- Visualized and monitored DAG execution in the Airflow UI.

**Proficiencies Used:** Apache Airflow, Python, Amazon S3, Amazon Redshift Serverless, SQL, ETL, AWS IAM, DAG Scheduling, VS Code

---

## Technologies Used Across the Nanodegree
- **Programming & Query Languages:** Python, SQL, CQL
- **Databases:** PostgreSQL, Apache Cassandra, Amazon Redshift, Amazon Redshift Serverless
- **Big Data & Cloud Tools:** Apache Airflow, Apache Spark, AWS Glue, AWS S3, AWS IAM, AWS EC2, Amazon Athena
- **Data Modeling:** Star Schema, Snowflake Schema, Normalization, Denormalization
- **Development Tools:** VS Code, AWS CLI, Airflow UI, Glue Studio

---

## Key Learnings
- Designing and implementing **data models** for both relational and NoSQL databases.
- Building **ETL pipelines** to extract, transform, and load data into optimized schemas for analytics.
- Leveraging **AWS cloud services** (S3, Redshift, Glue, Athena, IAM, EC2) for scalable data solutions.
- Processing big data using **Apache Spark** and **PySpark** for distributed computation.
- Implementing **data lake architectures** with Landing, Trusted, and Curated zones.
- Orchestrating complex workflows using **Apache Airflow** with custom reusable operators.
- Supporting **incremental (append)** and **full refresh (truncate)** load strategies in pipelines.
- Ensuring **data quality** with automated validation checks before publishing datasets.
- Applying **schema design best practices** for performance optimization in cloud warehouses.
- Using **VS Code** and other modern development tools for collaborative, production-grade projects.
