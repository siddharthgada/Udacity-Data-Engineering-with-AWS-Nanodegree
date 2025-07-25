import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Amazon S3
AmazonS3_node1753288410388 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://sid-stedi-lakehouse/customer/landing/"], "recurse": True}, transformation_ctx="AmazonS3_node1753288410388")

# Script generated for node SQL Query
SqlQuery156 = '''
select * from myDataSource
where shareWithResearchAsOfDate is not null
'''
SQLQuery_node1753288508541 = sparkSqlQuery(glueContext, query = SqlQuery156, mapping = {"myDataSource":AmazonS3_node1753288410388}, transformation_ctx = "SQLQuery_node1753288508541")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SQLQuery_node1753288508541, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1753288380316", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1753288540889 = glueContext.getSink(path="s3://sid-stedi-lakehouse/customer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1753288540889")
AmazonS3_node1753288540889.setCatalogInfo(catalogDatabase="stedi_2",catalogTableName="customer_trusted")
AmazonS3_node1753288540889.setFormat("json")
AmazonS3_node1753288540889.writeFrame(SQLQuery_node1753288508541)
job.commit()