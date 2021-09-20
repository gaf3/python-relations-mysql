import unittest
import unittest.mock

from relations_mysql import *


class TestAND(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        criteria = AND(EQ("totes", "maigoats"), EQ("toast", "myghost", invert=True))
        criteria.generate()
        self.assertEqual(criteria.sql, """(`totes`=%s AND `toast`!=%s)""")
        self.assertEqual(criteria.args, ["maigoats", "myghost"])

        criteria.generate(indent=2)
        self.assertEqual(criteria.sql, """(
  `totes`=%s AND
  `toast`!=%s
)""")

        criteria.generate(indent=2, count=1)
        self.assertEqual(criteria.sql, """(
    `totes`=%s AND
    `toast`!=%s
  )""")

        criteria.generate(indent=2, count=2)
        self.assertEqual(criteria.sql, """(
      `totes`=%s AND
      `toast`!=%s
    )""")


class TestOR(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        criteria = OR(EQ("totes", "maigoats"), EQ("toast", "myghost", invert=True))
        criteria.generate()
        self.assertEqual(criteria.sql, """(`totes`=%s OR `toast`!=%s)""")
        self.assertEqual(criteria.args, ["maigoats", "myghost"])

        criteria.generate(indent=2)
        self.assertEqual(criteria.sql, """(
  `totes`=%s OR
  `toast`!=%s
)""")

        criteria.generate(indent=2, count=1)
        self.assertEqual(criteria.sql, """(
    `totes`=%s OR
    `toast`!=%s
  )""")

        criteria.generate(indent=2, count=2)
        self.assertEqual(criteria.sql, """(
      `totes`=%s OR
      `toast`!=%s
    )""")


class TestHAS(unittest.TestCase):

    def test_generate(self):

        criteria = HAS("totes", ["mai", "goats"])

        criteria.generate()
        self.assertEqual(criteria.sql, """JSON_CONTAINS(`totes`,CAST(%s AS JSON))""")
        self.assertEqual(criteria.args, ['["mai", "goats"]'])


class TestANY(unittest.TestCase):

    def test_generate(self):

        criteria = ANY("totes", ["mai", "goats"])

        criteria.generate()
        self.assertEqual(criteria.sql, """(JSON_CONTAINS(`totes`,CAST(%s AS JSON)) OR JSON_CONTAINS(`totes`,CAST(%s AS JSON)))""")
        self.assertEqual(criteria.args, ['["mai"]', '["goats"]'])


class TestALL(unittest.TestCase):

    def test_generate(self):

        criteria = ALL("totes", ["mai", "goats"])

        criteria.generate()
        self.assertEqual(criteria.sql, """(JSON_CONTAINS(`totes`,CAST(%s AS JSON)) AND JSON_LENGTH(`totes`)=JSON_LENGTH(CAST(%s AS JSON)))""")
        self.assertEqual(criteria.args, ['["mai", "goats"]', '["mai", "goats"]'])


class TestOP(unittest.TestCase):

    def test_generate(self):

        criteria = OP("totes__null", True)

        criteria.generate()
        self.assertEqual(criteria.sql, """`totes` IS NULL""")
        self.assertEqual(criteria.args, [])

        criteria = OP(totes__a__null=False)

        criteria.generate()
        self.assertEqual(criteria.sql, """`totes`->>%s IS NOT NULL""")
        self.assertEqual(criteria.args, ['$.a'])

        criteria = OP(totes__a__not_null=True)

        criteria.generate()
        self.assertEqual(criteria.sql, """`totes`->>%s IS NOT NULL""")
        self.assertEqual(criteria.args, ['$.a'])

        criteria = OP(totes__a__not_has=[1, 2, 3])

        criteria.generate()
        self.assertEqual(criteria.sql, """NOT JSON_CONTAINS(`totes`->>%s,CAST(%s AS JSON))""")
        self.assertEqual(criteria.args, ['$.a', '[1, 2, 3]'])

        criteria = OP(totes=1, JSONIFY=True)

        criteria.generate()
        self.assertEqual(criteria.sql, """CAST(`totes` AS JSON)=CAST(%s AS JSON)""")
        self.assertEqual(criteria.args, ['1'])

        self.assertRaisesRegex(relations_sql.SQLError, "need single pair", OP, "nope")

        criteria = OP(totes__a__null=False, EXTRACTED=True)

        criteria.generate()
        self.assertEqual(criteria.sql, """`totes__a` IS NOT NULL""")
        self.assertEqual(criteria.args, [])

        criteria = OP(totes__a__has=1, EXTRACTED=True)

        criteria.generate()
        self.assertEqual(criteria.sql, """JSON_CONTAINS(`totes__a`,%s)""")
        self.assertEqual(criteria.args, [1])

        criteria = OP(totes__a__any=[1, 2], EXTRACTED=True)

        criteria.generate()
        self.assertEqual(criteria.sql, """(JSON_CONTAINS(`totes__a`,CAST(%s AS JSON)) OR JSON_CONTAINS(`totes__a`,CAST(%s AS JSON)))""")
        self.assertEqual(criteria.args, ['[1]', '[2]'])

        criteria = OP(totes__a__all=[1, 2], EXTRACTED=True)

        criteria.generate()
        self.assertEqual(criteria.sql, """(JSON_CONTAINS(`totes__a`,CAST(%s AS JSON)) AND JSON_LENGTH(`totes__a`)=JSON_LENGTH(CAST(%s AS JSON)))""")
        self.assertEqual(criteria.args, ['[1, 2]', '[1, 2]'])



        self.assertRaisesRegex(relations_sql.SQLError, "need single pair", OP, "nope")
