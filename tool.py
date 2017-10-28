#!/usr/bin/env python2.7
import psycopg2
from datetime import datetime


def conn(query):
    try:
        db = psycopg2.connect(database="news")
        c = db.cursor()
        c.execute(query)
        results = c.fetchall()
        db.close()
        return results
    except Exception as e:
        raise e


def articles():
    """ fuction to get the most popular three articles of all time"""
    query = """SELECT a.title, v.views
                FROM articles AS a
                JOIN artbyviews AS v
                ON a.slug = v.slug
                ORDER BY v.views DESC
                LIMIT 3;"""
    results = conn(query)
    print("The most popular three articles of all time:")
    for result in results:
        print("\t\"" + str(result[0])+"\" - " + str(result[1]) + " views")


def authors():
    """ fuction to get the most popular authors of all time."""
    query = """SELECT au.name, sum(v.views) AS views
                FROM artbyviews AS v
                INNER JOIN articles AS a
                ON v.slug = a.slug
                INNER JOIN authors AS au
                ON a.author = au.id
                GROUP BY au.name
                ORDER BY views DESC;"""
    results = conn(query)
    print("The most popular article authors of all time:")
    for result in results:
        print("\t"+str(result[0]) + " - " + str(result[1]) + " views")


def errors():
    """ function to get the day on which more than 1% of requests led to errors
    """
    query = """SELECT * FROM (
                SELECT e.day,
                ROUND((e.error*100)/CAST(t.total AS DECIMAL(10,2)),2) AS errors
                FROM totalview AS t
                JOIN errorview AS e ON t.day=e.day) AS t
                WHERE errors>1.0;"""
    results = conn(query)
    print("The day on which more than 1% of requests led to errors:")
    for day, errors in results:
        print("\t{0:%B %d, %Y} - {1}% errors".format(day, errors))

if __name__ == '__main__':
    articles()
    authors()
    errors()
