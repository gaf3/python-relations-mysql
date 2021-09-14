import unittest
import unittest.mock

from relations_mysql import *


class TestDDL(unittest.TestCase):

    maxDiff = None

    def test_class(self):

        self.assertEqual(DDL.QUOTE, """`""")
        self.assertEqual(DDL.STR, """'""")
        self.assertEqual(DDL.SEPARATOR, """.""")
        self.assertEqual(DDL.PLACEHOLDER, """%s""")
        self.assertEqual(DDL.JSONIFY, """CAST(%s AS JSON)""")
        self.assertEqual(DDL.PATH, """%s->>%s""")
