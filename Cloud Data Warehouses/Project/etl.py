#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


# In[ ]:


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()
'''This function loads data from AWS S3 into Redshift staging tables using the COPY command. copy_table_queries is a list of SQL COPY statements. 
Each query loads data from an S3 bucket into a staging table in Redshift. It extracts raw data from S3 storage, loads it into staging tables in Redshift and ensures committed transactions for data integrity.'''

# In[ ]:


def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()
''' This function loads data from staging tables into the final analytics tables in the Redshift database.'''

# In[ ]:


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

