import pendulum
import logging

from airflow.decorators import dag, task

@dag(
    schedule_interval='@hourly',
    start_date=pendulum.now()
)
def task_dependencies():

    @task()
    def hello_world():
        logging.info("Hello World")

    @task()
    def addition(first,second):
        logging.info(f"{first} + {second} = {first+second}")
        return first+second

    @task()
    def subtraction(first,second):
        logging.info(f"{first -second} = {first-second}")
        return first-second

    @task()
    def division(first,second):
        logging.info(f"{first} / {second} = {int(first/second)}")   
        return int(first/second)     

# TODO: call the hello world task function
    hello = hello_world()
# TODO: call the addition function with some constants (numbers)
    five_plus_five = addition(5,5)
# TODO: call the subtraction function with some constants (numbers)
    five_minus_five = subtraction(5,5)
# TODO: call the division function with some constants (numbers)
    eight_divided_by_2 = division(8,2)
# TODO: create the dependency graph for the first three tasks
    hello >> five_plus_five
    hello >> five_minus_five
    five_plus_five >> eight_divided_by_2
    five_minus_five >> eight_divided_by_2
# TODO: Configure the task dependencies such that the graph looks like the following:
#
#                    ->  addition_task
#                   /                 \
#   hello_world_task                   -> division_task
#                   \                 /
#                    ->subtraction_task

#  TODO: assign the result of the addition function to a variable
    sum = addition(5,5)
#  TODO: assign the result of the subtraction function to a variable
    difference = subtraction(10,8)
#  TODO: pass the result of the addition function, and the subtraction functions to the division function
    div = division(sum,difference)
# TODO: create the dependency graph for the last three tasks
    sum >> div
    difference >> div

task_dependencies_dag=task_dependencies()