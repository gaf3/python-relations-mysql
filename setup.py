#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
    name="python-relations-mysql",
    version="0.6.1",
    package_dir = {'': 'lib'},
    py_modules = [
        'relations_mysql',
        'relations_mysql.sql',
        'relations_mysql.expression',
        'relations_mysql.criterion',
        'relations_mysql.criteria',
        'relations_mysql.clause',
        'relations_mysql.query',
        'relations_mysql.ddl',
        'relations_mysql.column',
        'relations_mysql.index',
        'relations_mysql.table'
    ],
    install_requires=[]
)
