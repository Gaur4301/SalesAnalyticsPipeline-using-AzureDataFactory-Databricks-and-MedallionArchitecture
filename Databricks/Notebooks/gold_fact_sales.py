from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import StructType,StructField
#reading data from silver layer and creating df
df_src=spark.sql('SELECT * FROM parquet.`abfss://silver@cargauravdatalake.dfs.core.windows.net/raw-data`')
#reading data from all dimensions
df_model=spark.sql('select * from cars_catalog.gold.dim_model')
df_branch=spark.sql('select * from cars_catalog.gold.dim_branch')
df_dealer=spark.sql('select * from cars_catalog.gold.dim_dealer')
df_date=spark.sql('select * from cars_catalog.gold.dim_date')
#creating resultant df aftee joining with all dimensions to get dim_keys
df_result=df_src.join(df_model,on='model_id',how='left')\
                .join(df_branch,on='branch_id',how='left')\
                .join(df_dealer,on='dealer_id',how='left')\
                .join(df_date,on='date_id',how='left').select(df_src['Revenue'],df_src['Units_Sold'],df_src['revenue_per_unit'],df_model['dim_model_key'],df_branch['dim_branch_key'],df_dealer['dim_dealer_key'],df_date['dim_date_key'])
from delta.tables import DeltaTable
#writing data to gold layer
if spark.catalog.tableExists('cars_catalog.gold.fact_sales'):
    delta_table=DeltaTable.forPath(spark,'abfss://gold@cargauravdatalake.dfs.core.windows.net/fact_sales')
    delta_table.alias('dt').merge(df_result.alias('dr'),'dt.dim_model_key=dr.dim_model_key and dt.dim_branch_key=dr.dim_branch_key and dt.dim_dealer_key=dr.dim_dealer_key and dt.dim_date_key=dr.dim_date_key').whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
else:
    df_result.write.format('delta').option('path','abfss://gold@cargauravdatalake.dfs.core.windows.net/fact_sales').saveAsTable('cars_catalog.gold.fact_sales')