import unittest
import unittest.mock

from relations_mysql import *


class TestSQL(unittest.TestCase):

    maxDiff = None

    def test_class(self):

        self.assertEqual(SQL.QUOTE, """`""")
        self.assertEqual(SQL.STR, """'""")
        self.assertEqual(SQL.SEPARATOR, """.""")
        self.assertEqual(SQL.PLACEHOLDER, """%s""")
        self.assertEqual(SQL.JSONIFY, """CAST(%s AS JSON)""")
        self.assertEqual(SQL.PATH, """%s->>%s""")
