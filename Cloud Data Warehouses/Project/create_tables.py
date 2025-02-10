#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


# In[ ]:


def drop_tables(cur, conn):
    ''' This function runs the query to drop the tables from the database and ensures that the changes are saved'''
    for query in drop_table_queries:
        print("Dropping Tables: " + query)
        cur.execute(query)
        conn.commit()

# In[ ]:


def create_tables(cur, conn):
    ''' This function runs the query to create the tables and ensures that the changes are saved'''
    for query in create_table_queries:
        print("Creating Tables: " + query)        
        cur.execute(query)
        conn.commit()


# In[ ]:


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    print("Connected to Redshift")
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

