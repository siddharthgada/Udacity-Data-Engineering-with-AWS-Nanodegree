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
| Glue Job | Description|
|:---:|:---:|
| Customer Landing to Trusted.py | Filters customers with non-null shareWithResearchAsOfDate.|
| Accelerometer Landing to Trusted.py | Joins raw accelerometer data with customer_trusted using email.|
| Step Trainer Landing to Trusted.py | Filters IoT records for customers in customers_curated.|
| Customer Trusted to Curated.py | Joins customer_trusted with accelerometer_trusted to create customers_curated.|
| Machine Learning Curated.py | Joins step_trainer_trusted with accelerometer_trusted on sensorReadingTime.|

🔍 Row Counts (Validated via Athena)
 | Table	 | Row Count	 | Notes
 |:---:|:---:|:---:|
 | customer_landing	 | 956	 | Includes rows with missing shareWithResearchAsOfDate.
 | customer_trusted	 | 482   | Filtered to only consenting users.
 | accelerometer_landing | 	81,273	 | Raw accelerometer readings.
 | accelerometer_trusted | 	32,025	 | Only data from users who opted in.
 | step_trainer_landing | 	28,680	 | Raw IoT readings.
 | step_trainer_trusted	 | 14,460	 | Data filtered by presence in customers_curated.
 | customers_curated	 | 464	 | Joined customers with valid accelerometer data.
 | machine_learning_curated | 	34,437	 | Final dataset ready for ML.

📁 Project Structure:<br>
.
├── glue_jobs/
│   ├── customer_landing_to_trusted.py
│   ├── accelerometer_landing_to_trusted.py
│   ├── step_trainer_landing_to_trusted.py
│   ├── customer_trusted_to_curated.py
│   ├── machine_learning_curated.py
├── sql_ddls/
│   ├── customer_landing.sql
│   ├── accelerometer_landing.sql
│   └── step_trainer_landing.sql
├── screenshots/
│   ├── athena_queries/
│   └── glue_job_configs/
└── Readme.md

💡 Key Learnings: 
- Schema Evolution: Used Glue's dynamic schema update options for handling evolving JSON.
- Privacy-First Design: Ensured only users with explicit consent are retained throughout the pipeline.
- Efficient Joins in Glue Studio: SQL Transform nodes produced more consistent and performant outputs than built-in Join nodes.
- Partitioning & Filtering: Reduced unnecessary data writes by filtering and selecting relevant columns at each stage.

📊 Technologies & Tools Used: <br>
1. Apache Cassandra: NoSQL database to store and retrieve structured event data.
2. Python (Pandas): Used for processing the event data and handling the ETL pipeline.
3. Cassandra Query Language (CQL): Used for creating tables, inserting data, and querying the database.
