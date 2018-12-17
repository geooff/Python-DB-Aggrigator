import sys
import psycopg2
import datetime
import psycopg2.extras
from datetime import datetime

#Build args to pass into quiry(s)
def getArgs(input_end_range, input_start_range):
	return {
    'sales_table': '',
    'input_end_range': str(input_end_range),
    'input_start_range': str(input_start_range)
    }

#Get oldest date in sales tableof question
def getOldestDate(arg, cur):
	cur.execute(
	"""
    SELECT MIN(date)
	FROM %(sales_table)s;
	""", arg)
	result = cur.fetchall()
	
	try:
		oldest_date = datetime.datetime.strptime(str(result[0][0]), '%Y-%m-%d')
	except ValueError:
		oldest_date = datetime.datetime.now()
	
	return oldest_date

#Sum sales data for a given range
def sumSalesTable(arg, cur):
	cur.execute(
	"""
      SELECT
      ROUND(SUM(sales_dollars), 2)
      FROM %(sales_table)s
      WHERE date < %(input_end_range)s
        AND date > %(input_start_range)s;
      """, arg)
	result = cur.fetchall()
	
	try:
		result = float(result[0][0])
	except TypeError:
		result = 0

	return result

#Retrieve a list of tables to crawl
def getAllTables(cur, client):
	log("Fetching Sales Tables for Vendor: "+str(client))
	cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
	
	return cur.fetchall()

def getYoYSales(client, sampleRange=90):

	sample_range = sampleRange
	year_length = 365

	input_end_range = datetime.datetime.now()
	input_start_range = input_end_range - datetime.timedelta(days=year_length+sample_range)

	#Define postgres params
	conn = connectDB("RDS", "services_"+str(client))
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	#Get All Tables in DB for a given client
	all_tables = getAllTables(cur, client)

	#Get all sales tables for a given client
	sales_table = [j for i in all_tables for j in i if j.startswith('sales_')]

	log("Retreveing Data")
	arg = getArgs(input_end_range, input_start_range)

	outputResults = {}
	sum_ty = 0
	sum_ly = 0

	#Loop through sales table for a given vender to retrieve sales TY (3mo) & LY (3mo)
	for i in range(len(sales_table)):
		
		if len(sales_table[i].split("_")) != 3: 
			print "Ignoring sales table: "+str(sales_table[i])+" Invalid format"
			continue 
		
		try: 
			counterparty = int(sales_table[i].split("_")[1])
		except ValueError:
			continue 

		log("Retreveing Aggrigate Data for sales table: "+str(sales_table[i]))
		arg['sales_table'] = AsIs(sales_table[i])

		#Find oldest references date (current datetime - sample_range - year)
		oldest_sales_date = getOldestDate(arg, cur)

		#Need the oldest_sales_date to be older (less than) the input_start_range  
		if oldest_sales_date > input_start_range: 
			log("Sales table history doesn't satisfy specified input range")
			continue

		#Retrieve sum of up all results for TY sales tables
		arg['input_start_range'] = input_end_range - datetime.timedelta(days=sample_range)
		arg['input_end_range'] = input_end_range
		sum_ty_indiv = sumSalesTable(arg, cur)

		#Retrieve sum of up all results for LY sales tables
		arg['input_start_range'] = input_start_range
		arg['input_end_range'] = input_start_range + datetime.timedelta(days=sample_range)
		sum_ly_indiv = sumSalesTable(arg, cur)

		#Build output: Dict of list
		outputResults[sales_table[i]] = [sum_ty_indiv, sum_ly_indiv]

	return outputResults

# For Debug
if __name__ == "__main__":
  
	#Take client and set parameters
	client = sys.argv[1]
	getYoYSales(client)