from wordwise import Extractor
import mysql.connector
import json
from filterreviews import filter_reviews
conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 
import nltk
import spacy

nltk.download('punkt')

nlp = spacy.load('en_core_web_sm')

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nlp = spacy.load('en_core_web_sm')

def find_sentences_with_keyword(reviews, keyword):
    keyword = keyword.lower()
    sentences_with_keyword = []
    sentences = nltk.sent_tokenize(reviews)
    for sentence in sentences:
        doc = nlp(sentence)
        if any(token.text.lower() == keyword or token.lemma_.lower() == keyword for token in doc):
            sentences_with_keyword.append(sentence)
    return sentences_with_keyword


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
       #print(str(mod_string))

    commandlistcounter = 0
    counter = 0
    commandlistnew  = []
    commandlistnew.append(data)


   
    lengthofnames = len(names)

    if lengthofnames > 0:
       c.execute("DELETE FROM productnames2")

    for i in range(0,len(commandlistnew[0])):
       counter = counter + 1
       #print(i)
       #print(commandlistnew[0][i])
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
        #print(review1)
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
    #print(keywords)

    datelist = []
    ratinglist = []
    allreviews1 = []
    counter = 0

    for keyword in keywords:
        for row in reviews:
            reviewlist = {"product":row[0], "review":row[1], "date":row[2], "rating":row[4]}
            if keyword in reviewlist['review']:
                allreviews1.append(str(reviewlist['review']))
                newrating = round(float(str(reviewlist['rating'])),2)
                ratinglist.append(newrating)
                counter = counter + 1
            reviewlist = {}
        averagerating = str(sum(ratinglist)/(len(ratinglist)))
        allreviews1 =' '.join(allreviews1)
        #print(allreviews1)
        #print('\n')
        #sent_1 = str(sentiment.polarity_scores(allreviews1))
        sent_1 = str(sentiment.polarity_scores(find_sentences_with_keyword(allreviews1, keyword)))
        if len(find_sentences_with_keyword(allreviews1, keyword)) != 0:
            counter = len(find_sentences_with_keyword(allreviews1, keyword))
        print(find_sentences_with_keyword(allreviews1, keyword))

        c.execute("INSERT INTO keywords (keyword,Mentions,sentiment,averagerating) VALUES (%s,%s,%s,%s)",(keyword, counter, sent_1, averagerating))
        conn.commit()
        
        allreviews1 = []
        counter = 0
        ratinglist =[]

    conn.close()
    c.close()
    return 'test'

data = ['Fellowes Touch Screen Cleaning Wipes Suitable for Tablet, Smartphone, E-Reader and Gaming Screens - Pack of 20 Biodegradable Screen Wipes, 9933501']
print(keywordtable(data))