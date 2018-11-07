import psycopg2 as pg
from pprint import pprint 


class ConnectionAlreadyEstablished(Exception):
	pass

class DBConnection:
	__conn = None
	def __new__(self, dbname, dbhost, dbport, dbuser, dbpassword):
		if(DBConnection.__conn is None):
			DBConnection.__conn = pg.connect(database=dbname, host=dbhost, port=dbport, user=dbuser, password=dbpassword)
		else:
			raise ConnectionAlreadyEstablished

	
