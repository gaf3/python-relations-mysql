"""
Base SQL module for all of MySQL SQL
"""


class SQL: # pylint: disable=too-few-public-methods
    """
    Base class for every MySQL expression storing constants
    """

    QUOTE = '`'
    STR = "'"
    SEPARATOR = '.'
    PLACEHOLDER = "%s"
    JSONIFY = "CAST(%s AS JSON)"
    PATH = "%s->>%s"
