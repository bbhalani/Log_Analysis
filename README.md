# Logs Analysis
## Project Description
The user-facing newspaper site frontend itself, and the database behind it, are already built and running. This project is to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like. The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, the log analysis tool will answer questions about the site's user activity. The program written in this project will run from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answers to some questions.

## Getting Started

### Installation
- python 2.7.10 or later version
- The virtual machine - vagrant

### How to run the project
1. Download or clone the virtual machine configuration from:
[here](https://github.com/udacity/fullstack-nanodegree-vm) into a fresh new directory and start it from there
2. download the data from [newsdata](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), unzip the folder and momve newsdata.sql file into the vagrant directory, which is shared with your virtual machine configuration.

The database includes three tables:

- The authors table includes information about the authors of articles.
- The articles table includes the articles themselves.
- The log table includes one entry for each time a user has accessed the site.

As you explore the data, you may find it useful to take notes! Don't try to memorize all the columns. Instead, write down a description of the column names and what kind of values are found in those columns.

To build the reporting tool, you'll need to load the site's data into your local database.

To load the data, cd into the vagrant directory and use the command '''psql -d news -f newsdata.sql.'''

Here's what this command does:
- psql : the PostgreSQL command line program
- -d news : connect to the database named news which has been set up for you
- -f newsdata.sql : run the SQL statements in the file newsdata.sql

Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

create following views
'''sql
CREATE VIEW artbyviews AS
SELECT a.slug, count(*) AS views
FROM articles AS a
JOIN log AS l
ON '/article/' || a.slug = l.path
WHERE l.status = '200 OK'
GROUP BY a.slug
ORDER BY views DESC;
'''

'''sql
CREATE VIEW errorview AS
SELECT date(time) AS day,
count(*) AS error
FROM log
WHERE status= '404 NOT FOUND'
GROUP BY day;
'''

'''sql
CREATE VIEW totalview AS
SELECT date(time) AS day,
count(*) AS total
FROM log
GROUP BY day ;
'''
run the python log analysis reporting tool
After the Views have been created, inside the virtual machine run tool.py with -
python tool.py
The python file tool.py executes 3 functions and prints the answers to the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?
