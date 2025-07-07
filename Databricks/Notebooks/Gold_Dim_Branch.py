from pyspark.sql import SparkSession
from pyspark.sql import functions as f
spark=SparkSession.builder.appName('Dimensions').getOrCreate()
#Creating paramters for the workspace
dbutils.widgets.text('incremental_flag','0')# 0 means full load and 1 means incremental load
incremental_flag=dbutils.widgets.get('incremental_flag')
print(incremental_flag)
#reading data from silver layer and creating df
df_src=spark.sql('SELECT distinct branch_id,branchname FROM parquet.`abfss://silver@cargauravdatalake.dfs.core.windows.net/raw-data`')
#Reading existing data from gold layer if not presnt creating schema
if spark.catalog.tableExists('cars_catalog.gold.dim_branch'):
  df_sink=spark.sql('Select * from cars_catalog.gold.dim_branch')
else:
  df_sink=spark.sql('select  1 as dim_branch_key,branch_id,branchname from parquet.`abfss://silver@cargauravdatalake.dfs.core.windows.net/raw-data` where 1=0')  
  #left join source df with sink to get new and updated records
df_join=df_src.join(df_sink,on='branch_id',how='left').select(df_src['branch_id'],df_src['branchname'],df_sink['dim_branch_key'])
df_join.display()
# Data frame containing new records
df_new=df_join.filter(df_join['dim_branch_key'].isNull()).select('branch_id','branchname')
display(df_new)
#Dataframe conatining updated records
df_update=df_join.filter(df_join['dim_branch_key'].isNotNull())
df_update.display()
#creating maximumid
if incremental_flag=='0':
    max_id=1
else:
    max_id=df_sink.agg(f.max('dim_branch_key').alias('max_id')).collect()[0][0]+1

df_new=df_new.withColumn('dim_branch_key',max_id+f.monotonically_increasing_id())
df_new.display()
df_output=df_new.unionByName(df_update)
df_output.display()
from delta.tables import DeltaTable
#Incremental Run
if spark.catalog.tableExists('cars_catalog.gold.dim_branch'):
    delta_table=DeltaTable.forPath(spark,'abfss://gold@cargauravdatalake.dfs.core.windows.net/dim_branch')
    delta_table.alias('t').merge(df_output.alias('o'),'t.dim_branch_key=o.dim_branch_key').whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

else:
#Initial Run
    df_output.write.format('delta').option('path','abfss://gold@cargauravdatalake.dfs.core.windows.net/dim_branch').saveAsTable('cars_catalog.gold.dim_branch')