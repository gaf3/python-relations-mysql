import unittest
import unittest.mock


import pymysql.cursors

import ipaddress

import relations
import relations_sql
import relations_pymysql

class TestPyMySQL(unittest.TestCase):

    maxDiff = None

    def setUp(self):

        self.source = relations_pymysql.Source("PyMySQLSource", "test_source", host=os.environ["MYSQL_HOST"], port=int(os.environ["MYSQL_PORT"]))
        self.source.connection.cursor().execute("CREATE DATABASE IF NOT EXISTS `test_source`")

        shutil.rmtree("ddl", ignore_errors=True)
        os.makedirs("ddl", exist_ok=True)

    def tearDown(self):

        cursor = self.source.connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS `test_source`")
