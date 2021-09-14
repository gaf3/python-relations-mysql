"""–
Module for Column DDL
"""

# pylint: disable=unused-argument

import relations_sql
import relations_mysql


class TABLE(relations_mysql.DDL, relations_sql.TABLE):
    """
    TABLE DDL
    """

    NAME = relations_mysql.TABLE_NAME
    COLUMN = relations_mysql.COLUMN
    INDEX = relations_mysql.INDEX
    UNIQUE = relations_mysql.UNIQUE

    INDEXES = True

    RENAME = "RENAME TABLE %s TO %s"

    def schema(self, sql):
        """
        Change the schema
        """

        sql.append(self.RENAME % (self.name(definition=True), self.name()))

    def rename(self, sql):
        """
        Change the schema
        """

        if "schema" not in self.migration:
            self.schema(sql)
