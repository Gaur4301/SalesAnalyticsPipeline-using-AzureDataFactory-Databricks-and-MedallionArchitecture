from pyspark.sql import SparkSession
from pyspark.sql import functions as f
spark=SparkSession.builder.appName('Dimensions').getOrCreate()
#Creating paramters for the workspace
dbutils.widgets.text('incremental_flag','0')# 0 means full load and 1 means incremental load
incremental_flag=dbutils.widgets.get('incremental_flag')
print(incremental_flag)
#reading data from silver layer and creating df
df_src=spark.sql('SELECT distinct model_id,model_category FROM parquet.`abfss://silver@cargauravdatalake.dfs.core.windows.net/raw-data`')
#Reading existing data from gold layer if not presnt creating schema
if spark.catalog.tableExists('cars_catalog.gold.dim_model'):
  df_sink=spark.sql('Select * from cars_catalog.gold.dim_model')
else:
  df_sink=spark.sql('select  1 as dim_model_key,model_id,model_category from parquet.`abfss://silver@cargauravdatalake.dfs.core.windows.net/raw-data` where 1=0') 

#left join source df with sink to get new and updated records
df_join=df_src.join(df_sink,on='model_id',how='left').select(df_src['model_id'],df_src['model_category'],df_sink['dim_model_key'])
df_join.display()
# Data frame containing new records
df_new=df_join.filter(df_join['dim_model_key'].isNull()).select('model_id','model_category')
display(df_new)
#Dataframe conatining updated records
df_update=df_join.filter(df_join['dim_model_key'].isNotNull())
df_update.display()
#creating maximumid
if incremental_flag=='0':
    max_id=1
else:
    max_id=df_sink.agg(f.max('dim_model_key').alias('max_id')).collect()[0][0]+1

df_new=df_new.withColumn('dim_model_key',max_id+f.monotonically_increasing_id())
df_new.display()
df_output=df_new.unionByName(df_update)
df_output.display()
from delta.tables import DeltaTable
#Incremental Run
if spark.catalog.tableExists('cars_catalog.gold.dim_model'):
    delta_table=DeltaTable.forPath(spark,'abfss://gold@cargauravdatalake.dfs.core.windows.net/dim_model')
    delta_table.alias('t').merge(df_output.alias('o'),'t.dim_model_key=o.dim_model_key').whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

else:
#Initial Run
    df_output.write.format('delta').option('path','abfss://gold@cargauravdatalake.dfs.core.windows.net/dim_model').saveAsTable('cars_catalog.gold.dim_model')