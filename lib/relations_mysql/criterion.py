"""
Module for all Relations MySQL Criterions, pieces of Criteria
"""

import relations_sql
import relations_mysql


class CRITERION(relations_mysql.SQL, relations_sql.CRITERION):
    """
    CRITERION class, for comparing two values
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.VALUE


class NULL(relations_mysql.SQL, relations_sql.NULL):
    """
    For IS NULL and IS NOT NULL
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.VALUE


class EQ(relations_mysql.SQL, relations_sql.EQ):
    """
    For =
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.VALUE


class GT(relations_mysql.SQL, relations_sql.GT):
    """
    For >
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.VALUE


class GTE(relations_mysql.SQL, relations_sql.GTE):
    """
    For >=
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.VALUE


class LT(relations_mysql.SQL, relations_sql.LT):
    """
    For <
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.VALUE


class LTE(relations_mysql.SQL, relations_sql.LTE):
    """
    For <=
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.VALUE


class LIKE(relations_mysql.SQL, relations_sql.LIKE):
    """
    For fuzzy matching
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.VALUE


class START(relations_mysql.SQL, relations_sql.START):
    """
    For fuzzy matching end of string
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.VALUE


class END(relations_mysql.SQL, relations_sql.END):
    """
    For fuzzy matching end of string
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.VALUE


class IN(relations_mysql.SQL, relations_sql.IN):
    """
    For IN
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.LIST
    VALUE = relations_mysql.VALUE


class CONTAINS(relations_mysql.SQL, relations_sql.CONTAINS):
    """
    Wether one set contains another
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.VALUE

    OPERAND = "JSON_CONTAINS(%s,%s)"


class LENGTHS(relations_mysql.SQL, relations_sql.LENGTHS):
    """
    Wether one set contains another
    """

    LEFT = relations_mysql.COLUMN_NAME
    RIGHT = relations_mysql.VALUE

    OPERAND = "JSON_LENGTH(%s)=JSON_LENGTH(%s)"
