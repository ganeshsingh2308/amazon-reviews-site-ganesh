from wordwise import Extractor
import mysql.connector

conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def keywordtable1(data,keywordlist):
    conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 

    sentiment = SentimentIntensityAnalyzer()

    allreviews = []

    c = conn.cursor()



    query = ''
    newquery = ''
    if  len(data) > 0:
        query = "SELECT * FROM reviews1 WHERE "
        productquery = " product=('"
        productquery2 = "')"

        

        if len(data) == 1:
            newquery = productquery  + data[0] + productquery2

        elif len(data) > 1:
            for i in range(0,len(data)):
              newquery += productquery  + data[i] + productquery2 
              if i+1 != len(data):
                newquery += "OR"


        
    
    finalquery = query + newquery

    c.execute(finalquery)
    reviews = c.fetchall()
    reviewcounter = 0

    

    for row in reviews:
        reviewcounter = reviewcounter + 1
        review = {"product":row[0], "review":row[1], "date":row[2], "rating":row[3]}
        review1 = str(review['review'])
        # review2 = review1.lstrip(review1[0]).rstrip(review1[-1])
        print(review1)
        allreviews.append(review1)
    
    print(reviewcounter)

    allreviews =' '.join(allreviews)

    conn.commit()

    keywords = keywordlist

    

    datelist = []
    ratinglist = []
    allreviews1 = []
    counter = 0

    for keyword in keywords:
        for row in reviews:
            reviewlist = {"product":row[0], "review":row[1], "date":row[2], "rating":row[3]}
            if keyword in reviewlist['review']:
                allreviews1.append(str(reviewlist['review']))
                newrating = float(str(reviewlist['rating']).replace(' out of 5 stars', ''))
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




