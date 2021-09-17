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

    def create(self, indent=0, count=0, pad=' ', **kwargs): # pylint: disable=too-many-locals
        """
        CREATE DLL
        """

        inside = []

        columns = []
        indexes = []

        for migration in self.migration["fields"]:
            if "inject" in migration:
                continue
            columns.append(self.COLUMN(migration=migration))
            if "extract" in migration:
                for extract in sorted(migration["extract"]):
                    store = migration.get("store", migration["name"])
                    columns.append(self.COLUMN(store=f"{store}_{extract}", kind=migration["extract"][extract]))

        table = {} if self.INDEXES else {"table": self.migration["name"], "schema": self.migration.get("schema")}

        if self.migration.get('id') is not None:
            indexes.append(relations_sql.SQL(f"PRIMARY KEY ({self.quote(self.migration['id'])})"))

        for index in sorted(self.migration.get("index", {})):
            indexes.append(self.INDEX(name=index, columns=self.migration["index"][index], **table))

        for index in sorted(self.migration.get("unique", {})):
            indexes.append(self.UNIQUE(name=index, columns=self.migration["unique"][index], **table))

        self.express(columns, inside, indent=indent, count=count+1, pad=pad)

        self.express(indexes, inside, indent=indent, count=count+1, pad=pad)

        one = pad * indent
        migration = pad * (count * indent)
        next = migration + one
        line = "\n" if indent else ""
        delimitter = f",{line}{next}"

        sql = [f"CREATE TABLE IF NOT EXISTS {self.name()} ({line}{next}{delimitter.join(inside)}{line})"]

        delimitter = f";\n\n{migration}"

        self.sql = f"{delimitter.join(sql)};\n"

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
