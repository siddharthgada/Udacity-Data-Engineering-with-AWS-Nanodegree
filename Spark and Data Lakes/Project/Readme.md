# 🧠 AWS Glue Data Lake Project for Health & Fitness Tracking
This repository contains my solution for a serverless data lake project using AWS Glue, Athena, and S3. The project simulates real-world data engineering tasks by ingesting JSON data from multiple sources, performing ETL transformations, filtering PII, and organizing the data into Landing, Trusted, and Curated zones.

## 🚀 Project Overview:<br>

This project demonstrates a modern data lake architecture using AWS Glue to process and transform raw JSON data stored in S3 into clean, queryable formats accessible through Amazon Athena. The data represents customers, accelerometer sensor readings, and step trainer devices.

## ✅ Project Pipeline <br>

🧾 Data Sources (Landing Zone): <br>
- Raw JSON files are ingested into Amazon S3 from: <br>
    - Website Form: customer_landing <br>
    - Mobile App: accelerometer_landing <br>
    - IoT Device: step_trainer_landing
  
## 📥 Table Creation & Data Loading
- Created Landing Zone Glue tables for:
    - customer_landing
    - accelerometer_landing
    - steptrainer_landing
- Used AWS Glue to create the database and the above tables in the designated Glue Data Catalog Database.
- Loaded raw JSON data directly from Amazon S3 into these tables, enabling downstream ETL transformations and querying via Athena.
    
## 🛠 Glue Jobs
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

## 🛠 Glue Jobs Summary <br>
| Glue Job | Description|
|:---:|:---:|
| Customer Landing to Trusted.py | Filters customers with non-null shareWithResearchAsOfDate.|
| Accelerometer Landing to Trusted.py | Joins raw accelerometer data with customer_trusted using email.|
| Step Trainer Landing to Trusted.py | Filters IoT records for customers in customers_curated.|
| Customer Trusted to Curated.py | Joins customer_trusted with accelerometer_trusted to create customers_curated.|
| Machine Learning Curated.py | Joins step_trainer_trusted with accelerometer_trusted on sensorReadingTime.|

## 🔍 Row Counts (Validated via Athena)
 | Table	 | Row Count	 | Notes
 |:---:|:---:|:---:|
 | customer_landing	 | 956	 | Includes rows with missing shareWithResearchAsOfDate.
 | customer_trusted	 | 482   | Filtered to only consenting users.
 | customers_curated	 | 464	 | Joined customers with valid accelerometer data.
 | accelerometer_landing | 	81,273	 | Raw accelerometer readings.
 | accelerometer_trusted | 	40,981	 | Only data from users who opted in.
 | step_trainer_landing | 	28,680	 | Raw IoT readings.
 | step_trainer_trusted	 | 14,460	 | Data filtered by presence in customers_curated.
 | machine_learning_curated | 	43,681	 | Final dataset ready for Data Science Team.

## 📁 Project Structure:<br>

├── Data Sources/ <br>
│   ├── Accelerometer/ <br> 
│   ├──    ├── JSON Accelerometer data <br> 
│   ├── Customer/ <br> 
│   ├──    ├── JSON Customer data <br> 
│   ├── Step_Trainer/ <br> 
│   ├──    ├── JSON Step_Trainer data <br> 
├── Glue Jobs/ <br>
│   ├── Customer Landing to Trusted.py <br> 
│   ├── Accelerometer Landing to Trusted.py <br>
│   ├── Step Trainer Landing to Trusted.py<br>
│   ├── Customer Trusted to Curated.py<br>
│   ├── Machine Learning Curated.py<br>
├── SQL DDL/<br>
│   ├── customer_landing.sql<br>
│   ├── accelerometer_landing.sql<br>
│   └── steptrainer_landing.sql<br>
├── Screenshots/<br>
│   ├── Glue Studio Job configurations<br>
│   ├── Athena queries showing row counts and joins<br>
└── Readme.md

## 🛡️ AWS Configuration
1. IAM Role: Custom IAM roles were created with least-privilege access to allow Glue Jobs to read/write to specific S3 buckets.
2. VPC Endpoint: A VPC Gateway Endpoint was created for secure, high-throughput access from AWS Glue to S3, avoiding public internet.
3. 

## 💡 Key Learnings: 
1. Schema Evolution: Used Glue's dynamic schema update options for handling evolving JSON.
2. Privacy-First Design: Ensured only users with explicit consent are retained throughout the pipeline.
3. Efficient Joins in Glue Studio: SQL Transform nodes produced more consistent and performant outputs than built-in Join nodes.
4. Partitioning & Filtering: Reduced unnecessary data writes by filtering and selecting relevant columns at each stage.

## 📊 Technologies & Tools Used: <br>
1. AWS Glue Studio – Visual and code-based ETL orchestration
2. Amazon Athena – Querying structured data in S3
3. Amazon S3 – Scalable object storage for each data zone
4. JSON – Source data format

  ## 👤 Author

**Siddharth Gada**  
📧 Email: gadasiddharth@gmail.com <br>
🔗 LinkedIn: https://www.linkedin.com/in/siddharthgada/
