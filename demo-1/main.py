import pymysql
from config import conn_details
import argparse

def parse_args():
	#parsing command line arguments
	
	parser = argparse.ArgumentParser(description='Description of your program')
	parser.add_argument('-o','--operation', help='operation', required=True)
	
	parser.add_argument('-t','--table',help='table', required=True)
	
	parser.add_argument('-c','--col',help='column')

	parser.add_argument('-v','--value',help='values ex:1,1,song_name,minute')
	parser.add_argument('-b','--orderby',help='DESC')
	
	args = vars(parser.parse_args())
	
	return args

class Database():
	#Database class and its operations

	def __init__(self,conn_details):
		#connection details check config.py
		self.config=conn_details

		#establish connection
		self.__connect()

	def get_cursor(self):
		#return cursor to access the database
		return self.conn.cursor()

	def __connect(self):
		"""Connect to the database"""
		self.conn = pymysql.connect(host = self.config['host'], user = self.config['user'],
		                password = self.config['password'], db = self.config['db_name'])

	def show_contents(self,table):

		cur = self.get_cursor()

		statement = "select * from %s;"%(table)
		
		#execute statement using cursor
		cur.execute(statement)

		#get the output
		output = cur.fetchall()

		#showing output
		for row in output:
			print(row)

		# To close the connection
		self.conn.close()

	def insertvalues_Band(self,table,value):

		cur = self.get_cursor()

		statement = "insert into %s(band_name) values ('%s');"%(table,value)

		cur.execute(statement)

		# to insert
		self.conn.commit()

		# To close the connection
		self.conn.close()

	def selecttable_orderby(self,table,col,order):

		cur = self.get_cursor()

		statement = "select * from %s order by %s %s;"%(table,col,order)

		cur.execute(statement)

		#get the output
		output = cur.fetchall()

		#showing output
		for row in output:
			print(row)
		# To close the connection
		self.conn.close()


def main(args):
	
	db_obj = Database(conn_details)
	
	if args['operation'] == "select":

		db_obj.show_contents(args['table'])

	if args['operation'] == "insert":
		
		db_obj.insertvalues_Band(args['table'],args['value'])


	if args['operation'] == "orderby":

		if not args['orderby']:
			db_obj.selecttable_orderby(args['table'],args['value'],'')

		else:
			db_obj.selecttable_orderby(args['table'],args['value'],args['orderby'])


# Driver Code
if __name__ == "__main__" :
	args = parse_args()
	main(args)




