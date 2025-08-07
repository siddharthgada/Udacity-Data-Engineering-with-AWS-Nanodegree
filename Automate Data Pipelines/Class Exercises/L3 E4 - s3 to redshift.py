import pendulum
import logging

from airflow.decorators import dag, task
from airflow.secrets.metastore import MetastoreBackend
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator


# Use the PostgresHook to create a connection using the Redshift credentials from Airflow 
# Use the PostgresOperator to create the Trips table
# Use the PostgresOperator to run the LOCATION_TRAFFIC_SQL


from udacity.common import sql_statements

@dag(
    start_date=pendulum.now()
)
def load_data_to_redshift():


    @task
    def load_task():    
        metastoreBackend = MetastoreBackend()
        aws_connection=metastoreBackend.get_connection("aws_credentials")
        logging.info(vars(aws_connection))
# TODO: create the redshift_hook variable by calling PostgresHook()
        redshift_hook.run(sql_statements.COPY_ALL_TRIPS_SQL.format(aws_connection.login, aws_connection.password))

# TODO: create the create_table_task by calling PostgresOperator()
        create_table_task = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="redshift",
        sql=sql_statements.CREATE_TRIPS_TABLE_SQL
    )

# TODO: create the location_traffic_task by calling PostgresOperator()
        location_traffic_drop = PostgresOperator(
        task_id = "location_traffic_drop"
        postgres_conn_id="redshift",
        sql=sql_statements.LOCATION_TRAFFIC_SQL_DROP      
        )

        location_traffic_create = PostgresOperator(
        task_id = "location_traffic_create"
        postgres_conn_id="redshift",
        sql=sql_statements.LOCATION_TRAFFIC_SQL_CREATE      
        )   

    load_data = load_task()

# TODO: uncomment the dependency flow for these new tasks    
    create_table_task >> load_data
    load_data >> location_traffic_drop
    location_traffic_drop >> location_traffic_create
    
s3_to_redshift_dag = load_data_to_redshift()
