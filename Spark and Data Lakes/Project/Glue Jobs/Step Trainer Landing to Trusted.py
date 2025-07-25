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

# Script generated for node Customer Curated
CustomerCurated_node1753315037464 = glueContext.create_dynamic_frame.from_catalog(database="stedi_2", table_name="customer_curated", transformation_ctx="CustomerCurated_node1753315037464")

# Script generated for node Step Trainer Landing
StepTrainerLanding_node1753315094672 = glueContext.create_dynamic_frame.from_catalog(database="stedi_2", table_name="steptrainer_landing", transformation_ctx="StepTrainerLanding_node1753315094672")

# Script generated for node Change Schema
ChangeSchema_node1753314665950 = ApplyMapping.apply(frame=CustomerCurated_node1753315037464, mappings=[("serialnumber", "string", "c_serialnumber", "string"), ("sharewithpublicasofdate", "long", "sharewithpublicasofdate", "bigint"), ("sharewithresearchasofdate", "long", "sharewithresearchasofdate", "bigint"), ("registrationdate", "long", "registrationdate", "bigint"), ("sharewithfriendsasofdate", "long", "sharewithfriendsasofdate", "bigint"), ("lastupdatedate", "long", "lastupdatedate", "bigint")], transformation_ctx="ChangeSchema_node1753314665950")

# Script generated for node SQL Query
SqlQuery236 = '''
select * from st 
join c on serialnumber = c_serialnumber

'''
SQLQuery_node1753315326870 = sparkSqlQuery(glueContext, query = SqlQuery236, mapping = {"st":StepTrainerLanding_node1753315094672, "c":ChangeSchema_node1753314665950}, transformation_ctx = "SQLQuery_node1753315326870")

# Script generated for node SQL Query - Dropping unwanted cols from the join
SqlQuery235 = '''
select sensorReadingTime, serialNumber, distanceFromObject from myDataSource

'''
SQLQueryDroppingunwantedcolsfromthejoin_node1753301772082 = sparkSqlQuery(glueContext, query = SqlQuery235, mapping = {"myDataSource":SQLQuery_node1753315326870}, transformation_ctx = "SQLQueryDroppingunwantedcolsfromthejoin_node1753301772082")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SQLQueryDroppingunwantedcolsfromthejoin_node1753301772082, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1753300375073", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1753301847804 = glueContext.getSink(path="s3://sid-stedi-lakehouse/step_trainer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1753301847804")
AmazonS3_node1753301847804.setCatalogInfo(catalogDatabase="stedi_2",catalogTableName="step_trainer_trusted")
AmazonS3_node1753301847804.setFormat("json")
AmazonS3_node1753301847804.writeFrame(SQLQueryDroppingunwantedcolsfromthejoin_node1753301772082)
job.commit()