import requests
import json
import string
import time
import pymysql
from pycorenlp import StanfordCoreNLP
from bs4 import BeautifulSoup

def ginit():    
    db = pymysql.connect(host="localhost",user="root",password="Torres@09",db="ArticleGuardian")
    print(db)
    counter = 0
    cur = db.cursor()
    try:
        cur.execute("""ALTER TABLE `NewsBlocks_2014` CHANGE `NID` `NID` INT(250) NOT NULL;""")
        db.commit()
        print("Type change 1")
    except:
        db.rollback()

    cur.execute("""SELECT COUNT(NID) FROM NewsBlocks_2014;""")
    temp = cur.fetchone()
    print(temp)
    #counter = temp[0] + 1
    if(temp == None):
        counter = 0
    else:
        counter = temp[0] + 1
    print(counter)
    try:
        cur.execute("""ALTER TABLE `NewsBlocks_2014` CHANGE `NID` `NID` VARCHAR(250) NOT NULL;""")
        db.commit()
        print("Type change 2")
    except:
        db.rollback()

    try:
        for i in range(1,5000):
            url="https://content.guardianapis.com/search?"
            parameters = {
                'api-key' : "83f61516-4fde-4d5d-a404-f358a0003f59",
                'q' : 'politics OR technology',
                'show-fields' : 'headline,trailText,lastModified',
                'page' : i,
                'from-date' : '2014-01-02',
                'to-date' : '2014-12-31',
                'page-size' : 50,
                'order-by' : 'oldest'
            }
            r = requests.get(url,params=parameters)
            print(r.status_code)
            articledata_dict = json.loads(r.text)
            for j in range(0,50):
                newsblocks = articledata_dict['response']['results'][j]['fields']
                cleantext = BeautifulSoup(newsblocks['trailText'], 'html.parser').text
                try:
                    cur.execute("""INSERT INTO NewsBlocks_2014 VALUES (%s,%s,%s,%s,%s);""",(counter,newsblocks['headline'],cleantext,newsblocks['lastModified'],'NULL'))
                    db.commit()
                    counter+=1
                    print("Success")
                except Exception:
                    db.rollback()
                    print("Fuck ")
    except:
        print()
    cur.execute("""ALTER TABLE `NewsBlocks_2014` CHANGE `NID` `NID` INT(250) NOT NULL;""")
    db.commit()
    print("Type change 3")
    db.close()