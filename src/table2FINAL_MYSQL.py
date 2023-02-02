from wordwise import Extractor
import mysql.connector

conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment = SentimentIntensityAnalyzer()
from nltk.metrics.distance import edit_distance


def individual_keyword(keyword):

    allreviews = []
    conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 
    c = conn.cursor(buffered=True)
    c.execute("DELETE FROM keyword_specific")


    # c = conn.cursor(buffered=True)
    c.execute("SELECT * FROM productnames2")
    names = c.fetchall()
    conn.commit()
    c.execute("SELECT * FROM marketplace")
    marketplaces = c.fetchall()
    conn.commit()
    c.execute("SELECT * FROM vine")
    vines = c.fetchall()
    conn.commit()
    

    if names:
        pass

    namelist = []
    marketplacelist = []
    vinelist = []

    for count, name in enumerate(names):
        newname = str(name)
        size = len(newname)
        newname = newname[1:]
        mod_string = newname[:size - 3]
        namelist.append(str(mod_string))

    for count, marketplace in enumerate(marketplaces):
        newmarketplace = str(marketplace)
        size = len(newmarketplace)
        newmarketplace = newmarketplace[1:]
        mod_string = newmarketplace[:size - 3]
        marketplacelist.append(str(mod_string))

    for count, vine in enumerate(vines):
        newvine = str(vine)
        size = len(newvine)
        newvine = newvine[1:]
        mod_string = newvine[:size - 3]
        vinelist.append(str(mod_string))
    
    
    query = ''
    newquery = ''
    if  len(namelist) > 0:
        query = "SELECT * FROM reviews2 WHERE "
        productquery = "product=("
        productquery2 = ")"
        marketplacequery = "marketplace=("
        vinequery = "vine=("
        andquery = ") AND "

        

        #if len(namelist) == 1 and len(marketplacelist) == 1 and len(vinelist) == 1:
        #    newquery = productquery  + namelist[0] + productquery2 + andquery + marketplacequery + marketplacelist[0] + productquery2 + andquery + vinequery + vinelist[0] + productquery2

        if len(namelist) >= 1 and len(marketplacelist) >= 1 and len(vinelist) >= 1:
            for i in range(0,len(namelist)):
              if i == 0:
                newquery += "("  
              newquery += productquery  + namelist[i] + productquery2

              if i+1 != len(namelist):
                newquery += " OR "
              if i+1 == len(namelist):
                newquery += andquery
            for i in range(0,len(marketplacelist)):
              if i == 0:
                newquery += "("
              newquery += marketplacequery  + marketplacelist[i] + productquery2 
              if i+1 != len(marketplacelist):
                newquery += " OR "
              if i+1 == len(marketplacelist):
                newquery += andquery
            for i in range(0,len(vinelist)):
              if i == 0:
                newquery += "("
              newquery += vinequery  + vinelist[i] + productquery2 
              if i+1 != len(vinelist):
                newquery += " OR "
              if i+1 == len(vinelist):
                newquery += ")"
              

    # print(namelist)      
    # print(vinelist)
    # print(marketplacelist)
    #print(newquery)
    finalquery = query + newquery
    # print(newquery)
    # print(finalquery)  
    c.execute(finalquery)

    reviews = c.fetchall()
    conn.commit()
    # print(reviews)

    def find_similar_keyword(reviews, keyword):
        result = []
        for product, review, *rest in reviews:
            if keyword in review:
                result.append((product, review, *rest))
            else:
                for word in review.split():
                    if edit_distance(word.lower(), keyword.lower()) <= 2:
                        result.append((product, review, *rest))
                        break
        return result
    
    result = find_similar_keyword(reviews, keyword)
    for product, review, *rest in result:
        reviewdict = {'product':product,'review':review,'date':rest[0],'marketplace':rest[1],'rating':rest[2],'sentiment':rest[3],'vine':rest[4]}
        c.execute("INSERT INTO keyword_specific (product,review,date,marketplace,rating,sentiment,vine) VALUES (%s,%s,%s,%s,%s,%s,%s)",(product,review,rest[0],rest[1],rest[2],rest[3],rest[4]))
        conn.commit()
        print(reviewdict)
    

    
    conn.close()
    c.close()
    return