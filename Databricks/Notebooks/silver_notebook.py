#importing libraries
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import StructType,StructField,StringType,IntegerType,FloatType
#SparkSession Created
spark=SparkSession.builder.appName("SalesSilverModel").getOrCreate()
#Reading data from bronze layer
df=spark.read.format("parquet").load("abfss://bronze@cargauravdatalake.dfs.core.windows.net/raw-data/")
#adding transformation columns
columns={
    "model_category":f.split(f.col("Model_ID"),'-')[0],
    "revenue_per_unit":f.col("Revenue")/f.col("Units_Sold" )
}
df=df.withColumns(columns)
display(df.groupBy('Year','BranchName').agg(f.sum(f.col('Units_Sold')).alias("Total_units_sold")).orderBy("Year","BranchName",ascending=[True,False]))
# df.display()
#Writing data to silver layer
df.write.mode("overwrite").format("parquet").save("abfss://silver@cargauravdatalake.dfs.core.windows.net/raw-data/")