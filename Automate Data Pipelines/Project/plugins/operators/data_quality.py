from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 table = "",
                 schema = "",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.schema = schema
        self.table = table

    def execute(self, context):
        self.log.info('Starting DataQualityOperator')
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)

        column_query = f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = '{self.schema}' 
              AND table_name = '{self.table}';
        """

        columns = redshift.get_records(column_query)
        if not columns:
            raise ValueError(f"No columns found for table {self.schema}.{self.table}")

        null_columns = []
        for (col,) in columns:
            null_check_query = f"SELECT COUNT(*) FROM {self.schema}.{self.table} WHERE {col} IS NULL;"
            result = redshift.get_first(null_check_query)
            null_count = result[0]
            if null_count > 0:
                null_columns.append((col, null_count))
        
        if null_columns:
            message = "Found NULLs in the following columns:\n" + \
                      "\n".join([f"{col}: {count} NULLs" for col, count in null_columns])
            raise ValueError(message)
        else:
            self.log.info(f"No NULL values found in any column of table {self.schema}.{self.table}.")
