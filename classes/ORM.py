# -*- coding: utf-8 -*-
import psycopg2
import sys
import json
from pdb import set_trace as debug

#Constants
DB_NAME = sys.argv[1] if len(sys.argv) == 2 else 'test'

def get_keys_and_vals(**kwargs):
	keys = list(kwargs.keys() )
	vals = [kwargs[key] for key in keys ]
	return [keys, vals]

def get_keys(**kwargs):
	return list(kwargs.keys() )

def get_values(**kwargs):
	return list(kwargs.values() )

def do_get_json(filename='SuperHiddenFile.exe'):
	return json.load(open(filename, 'r'))

def do_assembly_connection_string(vals={}):
	"""
	Vals is a dictionary with the following format:
		usr_name, usr_passwd, psql_port, psql_db (db_name), hostname
	The string gotta follow the same format
		"dbname='' user=''' password='' host='' port=''"
	"""
	#vals = do_get_json('SuperHiddenFile.exe')
	connection_string = ("dbname='%s' user='%s' password='%s' host='%s' port='%s'" %
		(vals['psql_db'], vals['usr_name'], vals['usr_passwd'],
		vals['hostname'], vals['psql_port'])
		)
	return connection_string

def do_replace_chars(string, chars_to_rep="' ", key=''):
	for char in chars_to_rep:
		if char in string:
			string = string.replace(char, key)
	return string

def do_assembly_where(connector='or', **kwargs):
	# debug()
	vals = get_values(**kwargs)
	keys = get_keys(**kwargs)
	vals = do_replace_chars(list_to_string(vals), chars_to_rep=' ').split(',')
	keys = do_replace_chars(list_to_string(keys)).split(',')
	and_connector = (len(keys) == 1 ) and '' or ' %s ' % (connector)
	where_desc = 'WHERE '
	for index in range(len(vals)):
		where_desc += (
			"%s = %s" %
			(keys[index], vals[index])
			)
		if index != len(vals)-1:
			where_desc += and_connector
	# debug()
	return where_desc
	# for index in range(len(vals)):


def do_assembly_table(keys, values):
	table_desc = '( '
	for key, value in zip(keys, values):
		if table_desc != '( ':
			table_desc += ', '
		table_desc += ( str(key) + ' ' + str(value) )
	table_desc += ' )'
	return table_desc

# def do_assebly_query(columns=[]):
# 	query = ''
# 	for column in columns:
# 		query += str(column)


def list_to_string(list_):
	"""
	Receives a list an return a string with the contac of each item.
	If it is a string, it will be sorrunded by \'
	"""
	# str_vals = list(map(str, list) )
	res = ''
	for item in list_:
		if res != '':
			res += ', '
		if isinstance(item, str):
			res += str('\'' + item + '\'' + ' ')
		else:
			res += str(str(item) + ' ')
	return res

class ORM():
	def __init__(self):
		self.con = psycopg2.connect(do_assembly_connection_string(do_get_json()))
		self.cr = self.con.cursor()

	def do_create_table(self, table_name='default_table', **kwargs):
		"""
		Creates a table with the given name and the given parameters as a dictionary.
		The format of the dictionary is:
					column_name: data_type
		"""
		# Warning, vulnerable to sql injection, exploit later
		kwvals = get_keys_and_vals(**kwargs)
		table_desc = do_assembly_table(kwvals[0], kwvals[1] ) 
		self.cr.execute(
			"CREATE TABLE IF NOT EXISTS %s %s" %
			(table_name, table_desc)
		)
		self.con.commit()

	def do_insert(self, tablename, **kwargs):
		"""
		Insert into the tablename the values passed as a python dictionary
		The format of the dictionary is:
					column_name: data_type
		"""
		#print (					
		self.cr.execute(
			"INSERT INTO %s ( %s ) VALUES ( %s )" % 
			(tablename,
			list_to_string(get_keys(**kwargs)).replace('\'', ''),
			list_to_string(get_values(**kwargs))
			)
		)
		self.con.commit()

	def do_query(self, tablename, *args):
		"""
		Queries into the given table, with the given columns (as *args).
		Returns the fetched query.
		"""
		table_desc = list_to_string(args).replace('\'', '')
		self.cr.execute(
			"SELECT %s FROM %s" %
			(table_desc, tablename)
		)
		return self.cr.fetchall()

	def do_query_where(self, tablename, connector='or', *args, **kwargs):
		"""
		Queries into the given table, with the given columns (as *args).
		Returns the fetched query filtered by the columns.
		E.g.
			do_query_where('issues', 'or', 'name', 'descr', name='name')
		"""
		where_str = do_assembly_where(connector=connector, **kwargs)
		columns = do_replace_chars(list_to_string(list(args)), chars_to_rep="'")
		# debug()
		self.cr.execute ("SELECT %s FROM %s %s" %
				(columns, tablename, where_str))

		return self.cr.fetchall()


	def do_delete(self, tablename, **kwargs):
		val = list_to_string([ get_values(**kwargs)[0] ] )
		key = get_keys(**kwargs)[0]
		query = ( "DELETE FROM %s WHERE %s = %s" %
			(tablename, key, val) )
		self.cr.execute(query)
		#print (query)
		self.con.commit()

	def do_describe_tables(self):
		self.cr.execute("select * from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
		return self.cr.fetchall()

	def do_update(self, tablename, **kwargs):
		set_val = list_to_string(get_values(**kwargs)[0:1])
		where_val = list_to_string(get_values(**kwargs)[1:2])
		set_key = list_to_string(get_keys(**kwargs)[0:1]).replace('\'', '')
		where_key = list_to_string(get_keys(**kwargs)[1:2]).replace('\'', '')

		query = ("UPDATE %s SET %s = %s WHERE %s == %s" %
				(tablename, set_key, set_val, where_key, where_val) 
				)
		self.cr.execute(query)
		self.con.commit()




if __name__ == '__main__':
	print (DB_NAME)
	#print (get_keys(name='nam nam', nom='nom nom nom') )
	#print (get_values(name='nam nam', nom='nom nom nom') )
	# with ORMPackageResource() as orm_instance:
	# 	# orm_instance.do_insert('animals', name='Benito', age=2)
	# 	debug()
	# 	# pass