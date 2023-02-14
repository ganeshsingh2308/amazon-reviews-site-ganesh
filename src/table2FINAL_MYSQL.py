from wordwise import Extractor
import mysql.connector

conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment = SentimentIntensityAnalyzer()
from nltk.metrics.distance import edit_distance
from filterreviews import filter_reviews


def individual_keyword(keyword):
    
    allreviews = []
    conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 
    c = conn.cursor(buffered=True)
    
    c.execute("DELETE FROM keyword_specific")
    conn.commit()

    reviews = filter_reviews()
    conn.commit()
    #print(reviews)

    def search_reviews(keyword, reviews):
      modifiedkeyword = str(keyword.lower())
      print("keyword ",modifiedkeyword)
      result = []
      
      for review in reviews:
        print(review[1])
        if modifiedkeyword in review[1].lower():
            result.append(review)
      #print(result)      
      return result
    finaltable1 = search_reviews(keyword, reviews)
    #print(finaltable1)
    for finaltable in finaltable1:
      c.execute("INSERT INTO keyword_specific (product,review,date,marketplace,rating,sentiment,vine) VALUES (%s,%s,%s,%s,%s,%s,%s)",(finaltable[0],finaltable[1],finaltable[2],finaltable[3],finaltable[4],str(finaltable[5]),finaltable[6]))
      conn.commit()
        
    

    
    conn.close()
    c.close()
    return "data1"