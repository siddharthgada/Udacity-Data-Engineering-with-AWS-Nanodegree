from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator
from final_project_operators.stage_redshift import StageToRedshiftOperator
from final_project_operators.load_fact import LoadFactOperator
from final_project_operators.load_dimension import LoadDimensionOperator
from final_project_operators.data_quality import DataQualityOperator
from helpers.final_project_sql_statements import SqlQueries

default_args = {
    'owner': 'udac',
    'start_date': pendulum.now(),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'depends_on_past': False,
    'catchup': False,
    'email_on_retry': False,
    'email_on_failure': False
}

@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='@hourly'
)
def final_project():

    start_operator = DummyOperator(task_id='Begin_execution')

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        table = "staging_events",
        redshift_conn_id = "redshift",
        aws_credentials_id = "aws_credentials",
        s3_bucket = "siddharth-gada",
        s3_key = "log-data",
        data_format = 's3://siddharth-gada/log_json_path.json',
        delimeter = ",",
        create_table_sql = """
        DROP TABLE IF EXISTS staging_events;
        CREATE TABLE IF NOT EXISTS staging_events (
            artist VARCHAR(255),
            auth VARCHAR(50),
            firstName VARCHAR(255),
            gender VARCHAR(1),
            itemInSession INT,
            lastName VARCHAR(255),
            length FLOAT,
            level VARCHAR(50),
            location VARCHAR(255),
            method VARCHAR(25),
            page VARCHAR(35),
            registration BIGINT,
            sessionId INT,
            song VARCHAR(255),
            status INT,
            ts BIGINT,
            userAgent VARCHAR(255),
            userId INT
        );
        """
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        table = "staging_songs",
        redshift_conn_id = 'redshift',
        aws_credentials_id = "aws_credentials",
        s3_bucket = "siddharth-gada",
        s3_key = "song-data",
        data_format = "auto",
        create_table_sql = """
        DROP TABLE IF EXISTS staging_songs;
        CREATE TABLE IF NOT EXISTS staging_songs (
            num_songs INT,
            artist_id VARCHAR(50),
            artist_latitude FLOAT,
            artist_longitude FLOAT,
            artist_location VARCHAR(255),
            artist_name VARCHAR(255),
            song_id VARCHAR(50),
            title VARCHAR(255),
            duration FLOAT,
            year INT
        );
        """
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id = "redshift",
        aws_credentials_id = "aws_credentials",
        table = "songplays",
        sql_query = SqlQueries.songplay_table_insert,
        create_table_sql = """
        DROP TABLE IF EXISTS songplays;
        CREATE TABLE IF NOT EXISTS songplays (
            songplay_id VARCHAR PRIMARY KEY,
            start_time TIMESTAMP NOT NULL,
            userid INT NOT NULL,
            level VARCHAR,
            song_id VARCHAR,
            artist_id VARCHAR,
            sessionid INT NOT NULL,
            location VARCHAR,
            useragent VARCHAR
        );
        """
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id = "redshift",
        aws_credentials_id = "aws_credentials",
        table = "public.user",
        action = "truncate", 
        sql_query = SqlQueries.user_table_insert,
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS public.user (
            userid INT PRIMARY KEY,
            firstName VARCHAR(255),
            lastName VARCHAR(255),
            gender VARCHAR(1),
            level VARCHAR(50)
        );
        """
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id = "redshift",
        aws_credentials_id = "aws_credentials",
        table = "song",
        action = "truncate", 
        sql_query = SqlQueries.song_table_insert,
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS song (
            song_id VARCHAR(50) PRIMARY KEY,
            title VARCHAR(255),
            artist_id VARCHAR(50),
            year INT,
            duration FLOAT
        );
        """
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id = "redshift",
        aws_credentials_id = "aws_credentials",
        table = "artist",
        action = "truncate", 
        sql_query = SqlQueries.artist_table_insert,
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS artist (
            artist_id VARCHAR(50) PRIMARY KEY,
            artist_name VARCHAR(255),
            artist_location VARCHAR(255),
            artist_latitude FLOAT,
            artist_longitude FLOAT
        );
        """
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id = "redshift",
        aws_credentials_id = "aws_credentials",
        table = "time",
        action = "truncate", 
        sql_query = SqlQueries.time_table_insert,
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS time (
            start_time TIMESTAMP PRIMARY KEY,
            hour INT,
            day INT,
            week INT,
            month INT,
            year INT,
            weekday INT
        );
        """
    )

    check_user_dim = DataQualityOperator(
        task_id='Check_User_Dim',
        redshift_conn_id = "redshift",
        table = "user",
        schema = "public"
    )

    check_song_dim = DataQualityOperator(
        task_id='Check_Song_Dim',
        redshift_conn_id = "redshift",
        table = "song",
        schema = "public"
    )

    check_artist_dim = DataQualityOperator(
        task_id='Check_Artist_Dim',
        redshift_conn_id = "redshift",
        table = "artist",
        schema = "public"
    )

    check_time_dim = DataQualityOperator(
        task_id='Check_Time_Dim',
        redshift_conn_id = "redshift",
        table = "time",
        schema = "public"
    )

    end_operator = DummyOperator(task_id='End_execution')

    start_operator >> stage_events_to_redshift
    start_operator >> stage_songs_to_redshift
    stage_events_to_redshift >> load_songplays_table
    stage_songs_to_redshift >> load_songplays_table
    load_songplays_table >> load_user_dimension_table
    load_songplays_table >> load_song_dimension_table
    load_songplays_table >> load_artist_dimension_table
    load_songplays_table >> load_time_dimension_table
    load_user_dimension_table >> check_user_dim
    load_song_dimension_table >> check_song_dim
    load_artist_dimension_table >> check_artist_dim
    load_time_dimension_table >> check_time_dim
    check_time_dim >> end_operator
    check_artist_dim >> end_operator
    check_song_dim >> end_operator
    check_user_dim >> end_operator

final_project_dag = final_project()