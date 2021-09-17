import unittest
import unittest.mock

import relations
from relations_mysql import *


class TestCOLUMN(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        field = relations.Field(bool, name="flag", default=True)
        ddl = COLUMN(field.define())
        self.assertEqual(ddl.migration["default"], 1)

    def test_generate(self):

        field = relations.Field(bool, name="flag")
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, "`flag` TINYINT")
        self.assertEqual(ddl.args, [])

        field = relations.Field(int, name="id")
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, "`id` BIGINT")
        self.assertEqual(ddl.args, [])

        field = relations.Field(int, name="id", auto=True)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, "`id` BIGINT AUTO_INCREMENT")
        self.assertEqual(ddl.args, [])

        field = relations.Field(float, "price", store="_price", default=1.25, none=False)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """`_price` DOUBLE NOT NULL DEFAULT 1.25""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(str, "name", store="_name", default="Willy", none=False)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """`_name` VARCHAR(255) NOT NULL DEFAULT 'Willy'""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(dict, "data", store="_data", default={"a": 1}, none=False)
        ddl = COLUMN(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """`_data` JSON NOT NULL DEFAULT '{"a": 1}'""")
        self.assertEqual(ddl.args, [])

        ddl = COLUMN(store="data__a__0___1____2_____3", kind="str")

        ddl.generate()
        self.assertEqual(ddl.sql, """`data__a__0___1____2_____3` VARCHAR(255) AS (`data`->>$.a[0][-1]."2"."-3")""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(bool, name="flag")
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `flag` TINYINT""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(int, name="id")
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `id` BIGINT""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(float, "price", store="_price", default=1.25, none=False)
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `_price` DOUBLE NOT NULL DEFAULT 1.25""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(str, "name", store="_name", default="Willy", none=False)
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `_name` VARCHAR(255) NOT NULL DEFAULT 'Willy'""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(dict, "data", store="_data", default={"a": 1}, none=False)
        ddl = COLUMN(field.define(), added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `_data` JSON NOT NULL DEFAULT '{"a": 1}'""")
        self.assertEqual(ddl.args, [])

        ddl = COLUMN(store="data__a__0___1____2_____3", kind="str", added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD `data__a__0___1____2_____3` VARCHAR(255) AS (`data`->>$.a[0][-1]."2"."-3")""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(int, store="id", default=1, none=False)
        definition = {
            "store": "_id",
            "kind": "float",
            "default": 1.25,
            "none": True
        }
        ddl = COLUMN(field.define(), definition)

        ddl.generate()
        self.assertEqual(ddl.sql, """CHANGE `_id` `id` BIGINT NOT NULL DEFAULT 1""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(dict, "data", store="data", default={"a": 1}, none=False)
        definition = {
            "store": "data",
            "kind": "dict"
        }
        ddl = COLUMN(field.define(), definition)

        print(field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, """CHANGE `data` `data` JSON NOT NULL DEFAULT '{"a": 1}'""")
        self.assertEqual(ddl.args, [])

        field = relations.Field(bool, name="flag")
        ddl = COLUMN(definition=field.define())

        ddl.generate()
        self.assertEqual(ddl.sql, "DROP `flag`")
        self.assertEqual(ddl.args, [])
