#Guardian
Sentiment Score Analysis of Politics and Tech Articles
Language: Python 
Database: MySQL 
Querying Language: SQL 
Python Modules: time, bs4, pymysql, pycorenlp, requests, json, time, StanfordCoreNLP
Abstract:

Articles matching with the query parameter, politics/technology, were added to the database via Python modules and Guardian API. 
Subsequently, they were processed by the StanfordCoreNLP server to add a sentiment score to every news item (row in the database). 
Then a table was created to hold an average sentiment score for the years, (2008,2012,2017-18). At the end, all the files were placed inside a function
and the specific modules were imported into a main file to process the functionality together.
