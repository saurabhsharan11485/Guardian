from pycorenlp import StanfordCoreNLP
import pymysql

def gsentiment():
    db = pymysql.connect(host="localhost",user="root",password="Torres@09",db="ArticleGuardian")
    print(db)
    nlp = StanfordCoreNLP('http://localhost:9000')
    cur = db.cursor()
    cur.execute("""SELECT COUNT(NID) FROM NewsBlocks_2014;""")
    temp = cur.fetchone()
    counter = temp[0]
    while(counter>=0):
        try:
            cur.execute("""SELECT TrailText from NewsBlocks_2014 WHERE NID = %s;""",(counter))
            tmpabs = cur.fetchone()
            finabs = str(tmpabs[0])
            res = nlp.annotate(finabs,
                        properties={
                            'annotators': 'sentiment',
                            'outputFormat': 'json',
                            'timeout': 1000000000
                        })
            for s in res["sentences"]:
                print("%s" %(s["sentimentValue"]))
            score = s['sentimentValue']
            try:
                cur.execute("""UPDATE NewsBlocks_2014 SET Score = %s WHERE NID = %s;""",(score,counter))
                db.commit()
                print("Score inserted")
                counter-=1
            except:
                db.rollback()
                print("Score insertion failed")
        except:
            db.rollback()
            print("Fail")
            break
    db.close()