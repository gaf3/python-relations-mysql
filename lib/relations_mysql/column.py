"""
Module for Column DDL
"""

# pylint: disable=unused-argument

import json

import relations_sql
import relations_mysql

class COLUMN(relations_mysql.DDL, relations_sql.COLUMN):
    """
    COLUMN DDL
    """

    KINDS = {
        "bool": "TINYINT",
        "int": "BIGINT",
        "float": "DOUBLE",
        "str": "VARCHAR(255)",
        "json": "JSON"
    }

    COLUMN_NAME = relations_mysql.COLUMN_NAME

    AUTO = """AUTO_INCREMENT"""
    EXTRACT = """AS (%s)"""

    def __init__(self, migration=None, definition=None, added=False, **kwargs):

        super().__init__(migration, definition, added, **kwargs)

        if self.migration and self.migration.get("kind") == "bool" and "default" in self.migration:
            self.migration["default"] = int(self.migration["default"])

    def modify(self, **kwargs): # pylint: disable=arguments-differ
        """
        MODIFY DLL
        """

        sql = [self.name()]

        kind = self.migration.get("kind", self.definition["kind"])
        store = self.migration.get("store", self.definition["store"])
        none = self.migration.get("none", self.definition.get("none"))
        default = self.migration.get("default", self.definition.get("default"))

        sql.append(self.KINDS.get(kind, self.KINDS["json"]))

        if "__" in store:

            name, path = self.COLUMN_NAME.split(store)
            sql.append(self.EXTRACT % (self.PATH % (self.quote(name), self.str(self.COLUMN_NAME.walk(path)))))

        else:

            if not none:
                sql.append("NOT NULL")

            if default is not None:
                if not isinstance(default, (bool, int, float, str)):
                    default = json.dumps(default)
                quote = self.STR if isinstance(default, str) else ''
                sql.append(f"DEFAULT {quote}{default}{quote}")

        self.sql = " ".join(sql)

        self.sql = f"CHANGE {self.name(definition=True)} {self.sql}"
