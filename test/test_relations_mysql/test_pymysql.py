import unittest
import unittest.mock

import os
import json
import pymysql.cursors

import ipaddress

import relations
import relations_mysql


class Meta(relations.Model):

    SCHEMA = "test_pymysql"

    id = int,{"auto": True}
    name = str
    flag = bool
    spend = float
    people = set
    stuff = list
    things = dict, {"extract": "for__0____1"}
    push = str


class TestPyMySQL(unittest.TestCase):

    maxDiff = None

    def setUp(self):

        self.connection = pymysql.connect(
            cursorclass=pymysql.cursors.DictCursor, host=os.environ["MYSQL_HOST"], port=int(os.environ["MYSQL_PORT"])
        )
        self.connection.cursor().execute("CREATE DATABASE IF NOT EXISTS `test_pymysql`")

    def tearDown(self):

        self.connection.cursor().execute("DROP DATABASE IF EXISTS `test_pymysql`")

    def test_execute(self):

        cursor = self.connection.cursor()

        ddl = relations_mysql.TABLE(Meta.thy().define())

        ddl.generate(indent=2)

        cursor.execute(ddl.sql)

        query = relations_mysql.INSERT(
            "test_pymysql.meta"
        ).VALUES(**{
            "name": "yep",
            "flag": True,
            "spend": 1.1,
            "people": {"tom"},
            "stuff": [1, None],
            "things": {"a": 1}
        }).VALUES(
            name="dive",
            flag=False,
            spend=3.5,
            people={"tom", "mary"},
            stuff=[1, 2, 3, None],
            things={"a": {"b": [1, 2], "c": "sure"}, "4": 5, "for": [{"1": "yep"}]}
        )

        query.generate()

        cursor.execute(query.sql, query.args)

        def check(value, **kwargs):

            query = relations_mysql.SELECT(
                "name"
            ).FROM(
                "test_pymysql.meta"
            ).WHERE(
                **kwargs
            )

            query.generate()

            cursor.execute(query.sql, query.args)

            if cursor.rowcount != 1:
                name = None
            else:
                name = cursor.fetchone()["name"]

            self.assertEqual(name, value)

        check("yep", flag=True)

        check("dive", flag=False)

        check("dive", people={"tom", "mary"})

        check("dive", things={"a": {"b": [1, 2], "c": "sure"}, "4": 5, "for": [{"1": "yep"}]})

        check("dive", stuff__1=2)

        check("dive", things__a__b__0=1)

        check("dive", things__a__c__like="su")

        check("yep", things__a__b__null=True)

        check("dive", things____4=5)

        check(None, things__a__b__0__gt=1)

        check(None, things__a__c__notlike="su")

        check(None, things__a__d__null=False)

        check(None, things____4=6)

        check("dive", things__a__b__has=1)

        check(None, things__a__b__has=[1, 3])

        check("dive", things__a__b__any=[1, 3])

        check(None, things__a__b__any=[4, 3])

        check("dive", things__a__b__all=[2, 1])

        check(None, things__a__b__all=[3, 2, 1])

        check("dive", people__has="mary")

        check(None, people__has="dick")

        check("dive", people__any=["mary", "dick"])

        check(None, people__any=["harry", "dick"])

        check("dive", people__all=["mary", "tom"])

        check(None, people__all=["tom", "dick", "mary"])
