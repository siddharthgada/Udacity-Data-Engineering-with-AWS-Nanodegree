import logging
import pendulum

from airflow.decorators import dag, task

# @dag decorates the greet_task to denote it's the main function
@dag(
    start_date=pendulum.now().subtract(days=1)
)
def greet_flow():

#
# TODO: Uncomment the Welcome to Airflow 2 log statement below
#


    @task
    def hello_world():
        logging.info("Hello World!")
        logging.info("Welcome to Airflow 2!")

    hello_world_task=hello_world()    

greet_flow_dag=greet_flow()