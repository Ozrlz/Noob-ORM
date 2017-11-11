# -*- coding: utf-8 -*-

from classes import ORM

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