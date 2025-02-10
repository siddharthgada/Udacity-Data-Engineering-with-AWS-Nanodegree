#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


# In[ ]:


def drop_tables(cur, conn):
    for query in drop_table_queries:
        print("Dropping Tables: " + query)
        cur.execute(query)
        conn.commit()
''' This function iterates through the list of tables in the drop_table_queries(list of SQL DROP TABLE statements). It runs the query to drop the table from the database and ensures that the changes are saved'''

# In[ ]:


def create_tables(cur, conn):
    for query in create_table_queries:
        print("Creating Tables: " + query)        
        cur.execute(query)
        conn.commit()
''' This function iterates through the list of tables in the create_table_queries(list of SQL CREATE TABLE statements). It runs the query to create the table and ensures that the changes are saved'''

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

