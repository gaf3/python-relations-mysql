import unittest
import unittest.mock

import relations
from relations_mysql import *


class TestINDEX(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        ddl = INDEX(name="people", columns=["stuff", "things"])

        ddl.generate()
        self.assertEqual(ddl.sql, """INDEX `people` (`stuff`,`things`)""")
        self.assertEqual(ddl.args, [])

        ddl = INDEX(name="people", columns=["stuff", "things"], added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD INDEX `people` (`stuff`,`things`)""")
        self.assertEqual(ddl.args, [])

        ddl = INDEX(name="people", columns=["stuff", "things"], definition={"name": "persons"})

        ddl.generate()
        self.assertEqual(ddl.sql, """RENAME INDEX `persons` TO `people`""")
        self.assertEqual(ddl.args, [])

        ddl = INDEX(definition={"name": "persons"})

        ddl.generate()
        self.assertEqual(ddl.sql, "DROP INDEX `persons`")
        self.assertEqual(ddl.args, [])


class TestUNIQUE(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        ddl = UNIQUE(name="people", columns=["stuff", "things"])

        ddl.generate()
        self.assertEqual(ddl.sql, """UNIQUE `people` (`stuff`,`things`)""")
        self.assertEqual(ddl.args, [])

        ddl = UNIQUE(name="people", columns=["stuff", "things"], added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD UNIQUE `people` (`stuff`,`things`)""")
        self.assertEqual(ddl.args, [])

        ddl = UNIQUE(name="people", columns=["stuff", "things"], definition={"name": "persons"})

        ddl.generate()
        self.assertEqual(ddl.sql, """RENAME INDEX `persons` TO `people`""")
        self.assertEqual(ddl.args, [])

        ddl = UNIQUE(definition={"name": "persons"})

        ddl.generate()
        self.assertEqual(ddl.sql, "DROP INDEX `persons`")
        self.assertEqual(ddl.args, [])
