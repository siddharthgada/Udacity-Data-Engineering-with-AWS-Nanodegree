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

# Script generated for node Accelerometer Landing
AccelerometerLanding_node1753290560371 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://sid-stedi-lakehouse/accelerometer/landing/"], "recurse": True}, transformation_ctx="AccelerometerLanding_node1753290560371")

# Script generated for node Custome Trusted
CustomeTrusted_node1753290635082 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://sid-stedi-lakehouse/customer/trusted/"], "recurse": True}, transformation_ctx="CustomeTrusted_node1753290635082")

# Script generated for node Join
Join_node1753290708543 = Join.apply(frame1=AccelerometerLanding_node1753290560371, frame2=CustomeTrusted_node1753290635082, keys1=["user"], keys2=["email"], transformation_ctx="Join_node1753290708543")

# Script generated for node SQL Query
SqlQuery4039 = '''
select timestamp, user, x, y, z from myDataSource

'''
SQLQuery_node1753290745762 = sparkSqlQuery(glueContext, query = SqlQuery4039, mapping = {"myDataSource":Join_node1753290708543}, transformation_ctx = "SQLQuery_node1753290745762")

# Script generated for node Accelerometer Trusted
EvaluateDataQuality().process_rows(frame=SQLQuery_node1753290745762, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1753290525177", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AccelerometerTrusted_node1753290801740 = glueContext.getSink(path="s3://sid-stedi-lakehouse/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AccelerometerTrusted_node1753290801740")
AccelerometerTrusted_node1753290801740.setCatalogInfo(catalogDatabase="stedi_2",catalogTableName="accelerometer_trusted")
AccelerometerTrusted_node1753290801740.setFormat("json")
AccelerometerTrusted_node1753290801740.writeFrame(SQLQuery_node1753290745762)
job.commit()