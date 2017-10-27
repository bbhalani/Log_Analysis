#!/usr/bin/env python 2.7
import psycopg2
from datetime import datetime


# fuction to get the most popular three articles of all time
def articles():
    db = psycopg2.connect(database="news")
    c = db.cursor()
    query1 = """select a.title,v.views from articles as a join
    artbyviews as v on a.slug = v.slug order by v.views desc limit 3;"""
    c.execute(query1)
    results = c.fetchall()
    print("The most popular three articles of all time:")
    for result in results:
        print("\t\"" + str(result[0])+"\" - " + str(result[1]) + " views")
    db.close()


# fuction to get the most popular authors of all time
def authors():
    db = psycopg2.connect(database="news")
    c = db.cursor()
    query2 = """select au.name, sum(v.views) as views from artbyviews as v inner
                join articles as a on v.slug = a.slug inner join authors as au
                on a.author = au.id group by au.name order by views desc;"""
    c.execute(query2)
    results = c.fetchall()
    print("The most popular article authors of all time:")
    for result in results:
        print("\t"+str(result[0]) + " - " + str(result[1]) + " views")
    db.close()


# function to get the day on which more than 1% of requests led to errors
def errors():
    db = psycopg2.connect(database="news")
    c = db.cursor()
    query3 = """select * from (select e.day, round((e.error*100)/cast(t.total
                as decimal(10,2)),2) as errors from totalview as t join
                errorview as e on t.day=e.day) as t where errors>1.0;"""
    c.execute(query3)
    results = c.fetchall()
    print("The day on which more than 1% of requests led to errors:")
    for result in results:
        print("\t"+str(result[0].strftime("%b %d, %y")) + " - " +
              str(result[1]) + "% errors")
    db.close()

articles()
authors()
errors()
