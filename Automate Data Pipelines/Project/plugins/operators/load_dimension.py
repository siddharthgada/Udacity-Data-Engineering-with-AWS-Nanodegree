from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 aws_credentials_id = "",
                 table = "",
                 sql_query = "",
                 create_table_sql = "",
                 action = "",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.sql_query = sql_query
        self.action = action
        self.create_table_sql = create_table_sql

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        
        self.log.info('Dropping and Creating {self.table} table')
        redshift.run(self.create_table_sql)

        # Truncate table if action is 'truncate'
        if self.action == "truncate":
            self.log.info("Truncating table {self.table} before insert")
            redshift.run("DELETE FROM {}".format(self.table))
        elif self.action != "append":
            raise ValueError("Unsupported action: {self.action}. Use 'append' or 'truncate'.")

        self.log.info("Inserting data from Staging Table into Dimension Table")
        redshift.run("INSERT INTO {} {}".format(self.table, self.sql_query))

        self.log.info("Done: Data loaded on {} table.".format(self.table))