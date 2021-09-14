"""–
Module for Column DDL
"""

# pylint: disable=unused-argument

import relations_sql
import relations_mysql


class INDEX(relations_mysql.DDL, relations_sql.INDEX):
    """
    INDEX DDL
    """

    TABLE = relations_mysql.TABLE_NAME
    COLUMNS = relations_mysql.COLUMN_NAMES

    CREATE = "INDEX"
    MODIFY = "RENAME INDEX %s TO %s"


class UNIQUE(INDEX):
    """
    UNIQUE INDEX DDL
    """

    CREATE = "UNIQUE"
