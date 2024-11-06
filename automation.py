# Import libraries required for connecting to mysql
import mysql.connector
# Import libraries required for connecting to DB2 or PostgreSql
import psycopg2
# Connect to MySQL
mysql_conn = mysql.connector.connect(user='root', password='mysecretpassword',host='localhost',database='sales')
mysql_cursor = mysql_conn.cursor()
# Connect to DB2 or PostgreSql
dsn_hostname = 'localhost'
dsn_user='postgres'        # e.g. "abc12345"
dsn_pwd ='mysecretpassword'      # e.g. "7dBZ3wWt9XN6$o0J"
dsn_port ="5432"                # e.g. "50000" 
dsn_database ="sales"           # i.e. "BLUDB"

psql_conn = psycopg2.connect(
   database=dsn_database, 
   user=dsn_user,
   password=dsn_pwd,
   host=dsn_hostname, 
   port= dsn_port
)

psql_cursor = psql_conn.cursor()
# Find out the last rowid from DB2 data warehouse or PostgreSql data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database or PostgreSql.

def get_last_rowid():
	SQL = "SELECT rowid FROM sales_data ORDER BY rowid LIMIT 1"
	psql_cursor.execute(SQL)
	last_id = psql_cursor.fetchone()[0]
	return last_id


last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
	SQL = f"SELECT * FROM sales_data WHERE rowid > {rowid};"
	mysql_cursor.execute(SQL)
	records = mysql_cursor.fetchall()
	return records

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL into DB2 or PostgreSql data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database or PostgreSql.

def insert_records(records):
	try:
		for record in records:
			insert_sql = f"""
				INSERT INTO sales_data VALUES ({record[0]}, {record[1]}, {record[2]}, {record[3]})
			"""
			psql_cursor.execute(insert_sql)
		psql_conn.commit()
	except Exception as e:
		print("Error when insert records:", e)
		psql_conn.rollback()

insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
mysql_conn.close()
# disconnect from DB2 or PostgreSql data warehouse 
psql_conn.close()
# End of program