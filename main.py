# -*- coding: utf-8 -*-

from classes import ORM
from pdb import set_trace as debug

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
		self._object = ORM.ORM()
		return self._object

	def __exit__(self, exc_type, exc_value, traceback):
		self._object.con.close()

if __name__ == '__main__':
	with ORMPackageResource() as orm:
		# orm_instance.do_insert('animals', name='Benito', age=2)
		debug()
		# print( orm.do_query_where('issues', 'name', 'descr', name='name') )
		# pass