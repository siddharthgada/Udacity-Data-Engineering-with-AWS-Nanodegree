# 🎶 Data Pipelines with Apache Airflow – Sparkify ETL Automation
This project automates the data pipeline for Sparkify, a fictional music streaming company, using Apache Airflow to orchestrate and monitor the ETL process. The pipeline extracts user activity and song data from AWS S3, stages it in Amazon Redshift, transforms it into a star-schema, and performs data quality checks for analytical reporting.

## 🚀 Project Goals:<br>
- Design and implement dynamic, reusable, and monitorable ETL pipelines using Airflow
- Load log and song data from S3 into Redshift staging tables
- Transform staged data into star-schema fact and dimension tables
- Implement custom Airflow operators for staging, loading and data quality validation
- Enable backfilling, incremental loads and data quality monitoring

## 🛠️ Tools & Technologies: <br>
- Apache Airflow – For orchestration and scheduling of ETL pipelines
- Amazon Redshift Serverless – As the data warehouse for storing staging, fact and dimension tables
- Amazon S3 – For storing raw JSON log and song data
- AWS IAM – For managing access and credentials
- Python – For writing custom Airflow operators and scripts
- PostgresHook (Airflow) – To interact with Redshift using SQL
- VS Code – Primary IDE for developing DAGs, custom operators and project configuration
- Airflow UI – For monitoring DAG runs, viewing logs and triggering tasks manually

## 📁 Project Structure:<br>
. <br>
├── dags/<br>
│   └── sparkify_dag.py  <br>            # Main Airflow DAG
├── plugins/<br>
│   └── helpers/<br>
│       └── sql_queries.py <br>         # SQL transformations
│   └── operators/<br>
│       ├── stage_redshift.py <br>      # StageToRedshiftOperator
│       ├── load_fact.py      <br>      # LoadFactOperator
│       ├── load_dimension.py  <br>     # LoadDimensionOperator
│       └── data_quality.py    <br>     # DataQualityOperator
├── final_project_dag_graph.jpg <br>    # DAG visualization
└── Readme.md<br>

## ✅ Custom Airflow Operators: <br>
|Operator	| Purpose|
|:---:|:---:|
| StageToRedshiftOperator	| Loads JSON data from S3 into Redshift staging tables using COPY command. |
| LoadFactOperator	| Loads data into songplays fact table using append-only strategy. |
| LoadDimensionOperator |	Loads data into dimension tables (users, songs, artists, time) with truncate or append option. |
| DataQualityOperator	| Runs checks to validate table row counts and NULL constraints. |

## 🔍 Data Quality Checks: <br>
Each dimension table is validated for:
- No NULLs in any column of any dimension table

## 🔄 Integration with AWS Services: <br>
- Data is copied from Udacity’s S3 bucket to a user-owned S3 bucket
- Amazon Redshift Serverless is configured to ingest data using the COPY command from the S3 bucket
- Airflow connects to:
  - Redshift Serverless using the Postgres hook with a connection ID (e.g., redshift)
  - AWS using AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY through Airflow’s connections UI or environment variables

## 🗃️ Datasets: <br>
- Log Data: s3://udacity-dend/log_data
- Song Data: s3://udacity-dend/song-data
- JSON Path: log_json_path.json

NOTE: These datasets can be copied onto your own S3 bucket (in the same AWS region as Redshift Serverless) for optimal performance. - I did this.

## ⚙️ DAG Configuration: <br>
- DAG default arguments:
  - 'start_date': pendulum.now()
  - 'retries': 3
  - 'retry_delay': timedelta(minutes=5)
  - 'depends_on_past': False
  - 'catchup': False
  - 'email_on_retry': False
  - 'email_on_failure': False

## 🧑‍💻 How to Run:
- Create IAM User (to give access to Airflow UI)
- IAM User needs to have the following existing policies:
  - AdministratorAccess
  - AmazonRedshiftFullAccess
  - AmazonS3FullAccess
- Create an Access Key so that the credentials can be used to configure the AWS connection in Airflow
- Create IAM Role (to give full access to S3)
- IAM Role needs to have the following existing policies:
  - AmazonS3FullAccess
- Create a Redshift Serverless workspace and namespace
  - Associate IAM role created while configuring the workspace and namespace
  - Turn on enhanced VPC routing
  - Edit the workspace to be publicly accessible
  - Add an inbound rule to the VPC Security Group in EC2
    - Type = Custom TCP
    - Port range = 0 - 5500
    - Source = Anywhere-iPv4
- Configure S3 and copy source data to your own bucket
- Set up Airflow connections:
  - AWS credentials (Airflow Connections to AWS Account using the IAM User Access Key)
  - Redshift connection (Airflow Connections to AWS Redshift using workspace endpoint)
- Edit the S3_bucket and S3_key in the DAG to the bucket and key you created and have loaded the files in
- Run the DAG from Airflow UI
- Monitor task execution and logs

## 💡 Key Learnings: <br>
1. Dynamic DAG Design
Learned how to create dynamic and modular DAGs in Apache Airflow using reusable custom operators, which improved maintainability and scalability.
2. Custom Airflow Operators
Built custom Airflow operators to encapsulate business logic for staging, loading fact and dimension tables and performing data quality checks.
3. Amazon Redshift Serverless Integration
Gained experience configuring and using Redshift Serverless for loading and querying large datasets, and connecting Redshift to Airflow using Postgres hooks.
4. Incremental Data Loads
Implemented logic for append vs truncate loading strategies, with parameterized controls in dimension load operators to support historical and fresh data loads.
5. Data Quality Validation
Developed reusable data quality checks to ensure reliability of data pipelines, including null checks and row count assertions.
6. End-to-End AWS Workflow
Understood how various AWS services (S3, IAM and Redshift Serverless) work together in a data pipeline, including security and access configurations.

## 📈 Outcome: <br>
By implementing this project, I developed and deployed a fully-automated and monitored ETL pipeline using Airflow, with dynamic tasks, reusable operators and strong data validation to ensure reliable reporting.

## 👤 Author

**Siddharth Gada**  
📧 Email: gadasiddharth@gmail.com <br>
🔗 LinkedIn: https://www.linkedin.com/in/siddharthgada/
