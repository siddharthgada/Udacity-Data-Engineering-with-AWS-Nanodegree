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
AccelerometerLanding_node1753294549901 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://sid-stedi-lakehouse/accelerometer/landing/"], "recurse": True}, transformation_ctx="AccelerometerLanding_node1753294549901")

# Script generated for node Customer Trusted
CustomerTrusted_node1753294522585 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://sid-stedi-lakehouse/customer/trusted/"], "recurse": True}, transformation_ctx="CustomerTrusted_node1753294522585")

# Script generated for node Join
Join_node1753294597227 = Join.apply(frame1=CustomerTrusted_node1753294522585, frame2=AccelerometerLanding_node1753294549901, keys1=["email"], keys2=["user"], transformation_ctx="Join_node1753294597227")

# Script generated for node SQL Query
SqlQuery4016 = '''
select DISTINCT serialNumber, shareWithPublicAsOfDate, shareWithResearchAsOfDate,
registrationDate, shareWithFriendsAsOfDate, lastupdatedate from myDataSource
where shareWithResearchAsOfDate is not null
'''
SQLQuery_node1753294651429 = sparkSqlQuery(glueContext, query = SqlQuery4016, mapping = {"myDataSource":Join_node1753294597227}, transformation_ctx = "SQLQuery_node1753294651429")

# Script generated for node Customer Curated
EvaluateDataQuality().process_rows(frame=SQLQuery_node1753294651429, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1753295240723", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
CustomerCurated_node1753295253501 = glueContext.getSink(path="s3://sid-stedi-lakehouse/customer/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="CustomerCurated_node1753295253501")
CustomerCurated_node1753295253501.setCatalogInfo(catalogDatabase="stedi_2",catalogTableName="customer_curated")
CustomerCurated_node1753295253501.setFormat("json")
CustomerCurated_node1753295253501.writeFrame(SQLQuery_node1753294651429)
job.commit()
