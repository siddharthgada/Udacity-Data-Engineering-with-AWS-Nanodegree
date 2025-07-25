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

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1753415817450 = glueContext.create_dynamic_frame.from_catalog(database="stedi_2", table_name="step_trainer_trusted", transformation_ctx="StepTrainerTrusted_node1753415817450")

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1753415851436 = glueContext.create_dynamic_frame.from_catalog(database="stedi_2", table_name="accelerometer_trusted", transformation_ctx="AccelerometerTrusted_node1753415851436")

# Script generated for node SQL Query
SqlQuery211 = '''
select sensorreadingtime, serialnumber, distancefromobject, x, y, z from st
join at on sensorreadingtime = timestamp
'''
SQLQuery_node1753415960739 = sparkSqlQuery(glueContext, query = SqlQuery211, mapping = {"st":StepTrainerTrusted_node1753415817450, "at":AccelerometerTrusted_node1753415851436}, transformation_ctx = "SQLQuery_node1753415960739")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SQLQuery_node1753415960739, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1753416357373", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1753416375305 = glueContext.getSink(path="s3://sid-stedi-lakehouse/machine_learning/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1753416375305")
AmazonS3_node1753416375305.setCatalogInfo(catalogDatabase="stedi_2",catalogTableName="machine_learning_curated")
AmazonS3_node1753416375305.setFormat("json")
AmazonS3_node1753416375305.writeFrame(SQLQuery_node1753415960739)
job.commit()