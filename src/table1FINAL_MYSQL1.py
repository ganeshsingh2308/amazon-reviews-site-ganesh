from wordwise import Extractor
import mysql.connector
import json
from filterreviews import filter_reviews
conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def keywordtable(data):
    conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 

    sentiment = SentimentIntensityAnalyzer()

    allreviews = []

    c = conn.cursor()
    c.execute("SELECT * FROM productnames2")
    names = c.fetchall()
    for name in names:
       newname = str(name)
       size = len(newname)
       newname = newname[1:]
       mod_string = newname[:size - 3]
       print(str(mod_string))

    commandlistcounter = 0
    counter = 0
    commandlistnew  = []
    commandlistnew.append(data)


   
    lengthofnames = len(names)

    if lengthofnames > 0:
       c.execute("DELETE FROM productnames2")

    for i in range(0,len(commandlistnew[0])):
       counter = counter + 1
       print(i)
       print(commandlistnew[0][i])
       c.execute("INSERT INTO productnames2 (product) VALUES (%s)",(json.loads("["+'"'+commandlistnew[0][i]+'"'+"]")))
       c.stored_results()
       conn.commit()


    reviews = filter_reviews()
    reviewcounter = 0

    

    for row in reviews:
        reviewcounter = reviewcounter + 1
        review = {"product":row[0], "review":row[1], "date":row[2], "rating":row[4]}
        review1 = str(review['review'])
        # review2 = review1.lstrip(review1[0]).rstrip(review1[-1])
        print(review1)
        allreviews.append(review1)
    
    print(reviewcounter)

    allreviews =' '.join(allreviews)

    conn.commit()

    c.execute("SELECT * FROM keywords")
    keywords1 = c.fetchall()
    conn.commit()


    if len(keywords1) > 0:
      c.execute("DELETE FROM keywords")
      conn.commit()

    keywordnumber = 0

    if 0 <= reviewcounter <= 100:
        keywordnumber = 10
    
    if 101 <= reviewcounter <= 500:
        keywordnumber = 20

    if  reviewcounter >= 501:
        keywordnumber = 30

    extractor = Extractor(spacy_model="en_core_web_trf")
    keywords = extractor.generate(allreviews,top_k=keywordnumber)
    print(keywords)

    datelist = []
    ratinglist = []
    allreviews1 = []
    counter = 0

    for keyword in keywords:
        for row in reviews:
            reviewlist = {"product":row[0], "review":row[1], "date":row[2], "rating":row[4]}
            if keyword in reviewlist['review']:
                allreviews1.append(str(reviewlist['review']))
                newrating = float(str(reviewlist['rating']))
                ratinglist.append(newrating)
                counter = counter + 1
            reviewlist = {}
        averagerating = str(sum(ratinglist)/(len(ratinglist)))
        allreviews1 =' '.join(allreviews1)
        sent_1 = str(sentiment.polarity_scores(allreviews1))
        c.execute("INSERT INTO keywords (keyword,Mentions,sentiment,averagerating) VALUES (%s,%s,%s,%s)",(keyword, counter, sent_1, averagerating))
        conn.commit()
        
        allreviews1 = []
        counter = 0
        ratinglist =[]

    conn.close()
    c.close()
    return 'test'

