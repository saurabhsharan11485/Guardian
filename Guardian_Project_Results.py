import pymysql

def gresults():
    db = pymysql.connect(host="localhost",user="root",password="Torres@09",db="ArticleGuardian")
    print(db)
    tables = ["NewsBlocks_2008","NewsBlocks_2012","NewsBlocks_2014","NewsBlocks_2017"]
    totscore = 0
    scoredict = {}

    for i in tables:
        scoredict[i] = {}

    cur = db.cursor()

    counterdict = {}
    for i in tables:
        counterdict[i] = {}


    cur.execute("""SELECT COUNT(TID) FROM SentimentScore""")
    tempcnt = cur.fetchone()
    tablecnt = tempcnt[0]
    c=int(tablecnt)


    for i in tables:
        print(i)
        cur.execute("""SELECT COUNT(NID) FROM {};""".format(i))
        temp = cur.fetchone()
        counter = temp[0] - 1
        counterdict[i] = counter
    print(counterdict)

    cur.execute("""SELECT TableName from SentimentScore""")
    temptbn = cur.fetchmany()

    for i in tables:
        if i in temptbn:
            print("Entered Continue")
            continue
        totscore = 0
        fincounter = counterdict[i]
        print(fincounter)
        while(fincounter >= 0):
            try:
                cur.execute("""SELECT Score FROM {} WHERE NID = {};""".format(i,fincounter))
                tmpscore = cur.fetchone()
                finscore = tmpscore[0]
                totscore += int(finscore)
                fincounter-=1
            except:
                print("Shit")
                break
        scoredict[i] = (totscore/(counterdict[i]+1))
        print(scoredict)
        try:
            print(i)
            print(c)
            cur.execute("""INSERT INTO SentimentScore VALUES (%s,%s,%s);""",(c,i,scoredict[i]))
            db.commit()
            print("Insertion successful")
            c+=1
        except:
            db.rollback()
            print("Insertion fucked")
    db.close()