import datetime
import csv
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from aggrigateSales import getYoY

#Iterate through all available tables in DB and return list
def getAllDB():
	#Get all DB in schema
	print "Fetching All available DB:"
	conn_base = connectDB("RDS")
	cur_base = conn_base.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur_base.execute("SELECT datname FROM pg_catalog.pg_database;")
	raw_db_list = cur_base.fetchall()
	
	db_list = []
	for string in raw_db_list:
		db_list.append(string[0])

	return db_list

#Get tables from DB
db_list = getAllDB()

#Import Data from Usage metrics
df_pen = pd.read_csv('UseageData.csv', index_col=0)

#Construct df_sales from sales
data = {}
for vender_id, row in df_pen.iterrows():
	if "services_"+str(vender_id) in db_list:
		data.update(getYoY(vender_id))

#Init df for Sales
df_sales = pd.DataFrame(data)

filename = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

#Return formatted CSV files for use in later data analytics
df_pen.to_csv(str(filename)+'_useage_data.csv')
df_sales.to_csv(str(filename)+'_sales_data.csv')