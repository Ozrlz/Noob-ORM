# -*- coding: utf-8 -*-
import sqlite3
import sys

#Constants
DB_NAME = sys.argv[1] if len(sys.argv) == 2 else 'test_default.db'

def get_keys_and_vals(**kwargs):
	keys = list(kwargs.keys() )
	vals = [kwargs[key] for key in keys ]
	return [keys, vals]

def get_keys(**kwargs):
	return list(kwargs.keys() )

def get_values(**kwargs):
	return list(kwargs.values() )

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
		self.con = sqlite3.connect(DB_NAME)
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
			'CREATE TABLE IF NOT EXISTS ' + table_name + ' ' +
			table_desc
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
			'INSERT INTO ' + tablename + 
			' (' + list_to_string(get_keys(**kwargs)).replace('\'', '') + ') ' +
			'VALUES (' + list_to_string(get_values(**kwargs)) + ')'
		)
		self.con.commit()

	def do_query(self, tablename, *args):
		"""
		Queries into the given table, with the given columns (as *args).
		Returns the fetched query.
		"""
		table_desc = list_to_string(args).replace('\'', '')
		self.cr.execute(
			'SELECT ' + table_desc + 'FROM ' + tablename
		)
		return self.cr.fetchall()

	def do_delete(self, tablename, **kwargs):
		val = list_to_string([ get_values(**kwargs)[0] ] )
		key = get_keys(**kwargs)[0]
		query = ("DELETE FROM " + tablename + " WHERE " + 
		key + " = " + val )
		self.cr.execute(query)
		#print (query)
		self.con.commit()


class ORMPackageResource():
	"""
	Class that represents an abstraction of an ORM as a package.
	If you want to use it you gotta make use of a \"with\" statement.
	e.g.
	with ORMPackageResource as orm:
		# orm.do_some_stuff()
	"""


	def __enter__(self):
		# __enter__ method
		self._object = ORM()
		return self._object

	def __exit__(self, exc_type, exc_value, traceback):
		self._object.con.close()


if __name__ == '__main__':
	print (DB_NAME)
	#print (get_keys(name='nam nam', nom='nom nom nom') )
	#print (get_values(name='nam nam', nom='nom nom nom') )
	with ORMPackageResource() as orm_instance:
		#orm_instance.do_insert('animals', name='Benito', age=2)
		pass