from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 redshift_conn_id = "",
                 aws_credentials_id = "",
                 table = "",
                 action = "append",
                 sql_query = "",
                 create_table_sql = "",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.action = action
        self.sql_query = sql_query
        self.create_table_sql = create_table_sql

    def execute(self, context):

        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)

        self.log.info('Dropping and Creating {self.table} table')
        redshift.run(self.create_table_sql)

        self.log.info("Inserting data from Staging Table into Fact Table")
        redshift.run("INSERT INTO {} {}".format(self.table, self.sql_query))
        
        self.log.info("Done: Data loaded on {} table.".format(self.table))