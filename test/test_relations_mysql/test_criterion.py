import unittest
import unittest.mock

from relations_mysql import *


class TestNULL(unittest.TestCase):

    def test_generate(self):

        criterion = NULL("totes", True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` IS NULL""")
        self.assertEqual(criterion.args, [])

        criterion = NULL(totes__a=False)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`->>%s IS NOT NULL""")
        self.assertEqual(criterion.args, ['$.a'])

    def test_generate(self):

        criterion = CRITERION("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` CRIERION %s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = CRITERION("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` CRIERIOFF %s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = CRITERION(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`#>>%s CRIERION JSON(%s)""")
        self.assertEqual(criterion.args, ['$."a"', '"maigoats"'])

        criterion = CRITERION(totes=test_expression.LIST([1, 2, 3]))

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` CRIERION (%s,%s,%s)""")
        self.assertEqual(criterion.args, [1, 2, 3])

        criterion.generate(indent=2)
        self.assertEqual(criterion.sql, """`totes` CRIERION (
  %s,
  %s,
  %s
)""")

        criterion.generate(indent=2, count=1)
        self.assertEqual(criterion.sql, """`totes` CRIERION (
    %s,
    %s,
    %s
  )""")

        criterion.generate(indent=2, count=2)
        self.assertEqual(criterion.sql, """`totes` CRIERION (
      %s,
      %s,
      %s
    )""")


class TestNULL(unittest.TestCase):

    def test_generate(self):

        criterion = NULL("totes", True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` IS NULL""")
        self.assertEqual(criterion.args, [])

        criterion = NULL(totes__a=False)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`->>%s IS NOT NULL""")
        self.assertEqual(criterion.args, ['$.a'])


class TestEQ(unittest.TestCase):

    def test_generate(self):

        criterion = EQ("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`=%s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = EQ("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`!=%s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = EQ(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`->>%s=CAST(%s AS JSON)""")
        self.assertEqual(criterion.args, ['$.a', '"maigoats"'])


class TestGT(unittest.TestCase):

    def test_generate(self):

        criterion = GT("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`>%s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = GT(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`->>%s>CAST(%s AS JSON)""")
        self.assertEqual(criterion.args, ['$.a', '"maigoats"'])


class TestGTE(unittest.TestCase):

    def test_generate(self):

        criterion = GTE("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`>=%s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = GTE(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`->>%s>=CAST(%s AS JSON)""")
        self.assertEqual(criterion.args, ['$.a', '"maigoats"'])


class TestLT(unittest.TestCase):

    def test_generate(self):

        criterion = LT("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`<%s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = LT(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`->>%s<CAST(%s AS JSON)""")
        self.assertEqual(criterion.args, ['$.a', '"maigoats"'])


class TestLTE(unittest.TestCase):

    def test_generate(self):

        criterion = LTE("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`<=%s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = LTE(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`->>%s<=CAST(%s AS JSON)""")
        self.assertEqual(criterion.args, ['$.a', '"maigoats"'])


class TestLIKE(unittest.TestCase):

    def test_generate(self):

        criterion = LIKE("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` LIKE %s""")
        self.assertEqual(criterion.args, ["%maigoats%"])

        criterion = LIKE("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` NOT LIKE %s""")
        self.assertEqual(criterion.args, ["%maigoats%"])

        criterion = LIKE(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`->>%s LIKE CAST(%s AS JSON)""")
        self.assertEqual(criterion.args, ['$.a', '"%maigoats%"'])


class TestSTART(unittest.TestCase):

    def test_generate(self):

        criterion = START("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` LIKE %s""")
        self.assertEqual(criterion.args, ["maigoats%"])

        criterion = START("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` NOT LIKE %s""")
        self.assertEqual(criterion.args, ["maigoats%"])

        criterion = START(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`->>%s LIKE CAST(%s AS JSON)""")
        self.assertEqual(criterion.args, ['$.a', '"maigoats%"'])


class TestEND(unittest.TestCase):

    def test_generate(self):

        criterion = END("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` LIKE %s""")
        self.assertEqual(criterion.args, ["%maigoats"])

        criterion = END("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` NOT LIKE %s""")
        self.assertEqual(criterion.args, ["%maigoats"])

        criterion = END(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`->>%s LIKE CAST(%s AS JSON)""")
        self.assertEqual(criterion.args, ['$.a', '"%maigoats"'])


class TestIN(unittest.TestCase):

    def test_generate(self):

        criterion = IN("totes", ["mai", "goats"])

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` IN (%s,%s)""")
        self.assertEqual(criterion.args, ["mai", "goats"])

        criterion = IN("totes", ["mai", "goats"], invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` NOT IN (%s,%s)""")
        self.assertEqual(criterion.args, ["mai", "goats"])

        criterion = IN(totes__a=["mai", "goats"])

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`->>%s IN (CAST(%s AS JSON),CAST(%s AS JSON))""")
        self.assertEqual(criterion.args, ['$.a', '"mai"', '"goats"'])

        criterion = IN(totes__a=[])

        criterion.generate()
        self.assertEqual(criterion.sql, """%s""")
        self.assertEqual(criterion.args, [False])


class TestCONTAINS(unittest.TestCase):

    def test_generate(self):

        criterion = CONTAINS("totes", ["mai", "goats"])

        criterion.generate()
        self.assertEqual(criterion.sql, """JSON_CONTAINS(`totes`,CAST(%s AS JSON))""")
        self.assertEqual(criterion.args, ['["mai", "goats"]'])


class TestLENGTHS(unittest.TestCase):

    def test_generate(self):

        criterion = LENGTHS("totes", ["mai", "goats"])

        criterion.generate()
        self.assertEqual(criterion.sql, """JSON_LENGTH(`totes`)=JSON_LENGTH(CAST(%s AS JSON))""")
        self.assertEqual(criterion.args, ['["mai", "goats"]'])
