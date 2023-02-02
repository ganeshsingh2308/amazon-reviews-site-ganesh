from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_cors import CORS

from flaskext.mysql import MySQL
import mysql.connector
import ast
from webscraper_FINAL_MYSQL import scrape_amazon
from scrapfly_webscraper import run
from TEST_data_to_JSON import outputtojson
from TEST_data_to_REMOVEBUTTON import removeproduct
from TEST_data_to_SQL_keyword import outputkeywordsort
from table1FINAL_MYSQL1 import keywordtable
from table2FINAL_MYSQL import individual_keyword
from table1FINAL_MYSQL2 import keywordtable1
from table1FINAL_MYSQL3 import allreviewtable
from livereload import Server
import time
import json
import asyncio
from TEST_vine_to_SQL import vinefilter
from TEST_marketplace_to_SQL import marketplacefilter
import datetime
from collections import defaultdict
from operator import itemgetter
from datetime import datetime


# Configure application
app = Flask(__name__, template_folder='templates')
CORS(app)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root123'
app.config['MYSQL_DATABASE_DB'] = 'main'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_REFRESH_EACH_REQUEST"] = True



#DASHBOARD


#scrapes the amazon link when a link is submitted
@app.route("/", methods = ['GET', 'POST'])
def process_json():
    
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json') and (request.method == 'POST'):
        data = request.get_json(force=True, cache=True)
        returnstate = ''
        conn = mysql.connect()
        conn.autocommit(True)
        c = mysql.get_db().cursor()
        c.execute("SELECT * FROM asinlist")
        names = c.fetchall()
        conn.commit()

        for i in names:
            newname = str(i).replace("('","")
            newname1 = newname.replace("',)","")

            if data['search'] == str(newname1):
                returnstate = "asin already here"
        print(data['search'])

        if returnstate == '':
            c.execute("INSERT INTO asinlist (asin) VALUES (%s)",(data['search']))
            conn.commit()
            asyncio.run(run(data['search'], data['country']))
        

        print(jsonify(returnstate))
        state1 = jsonify({'name':returnstate})
        

    
        return jsonify(returnstate)
        
    else:
        return 'data1'





#When the combination of products is selected then it will output a list of all the data for Number of reviews, average rating and positive/negative reviews
# @app.route("/test")
# def index():

#    try:
#     conn = mysql.connect()
#     conn.autocommit(True)
#     # c = conn.cursor(buffered=True)
#     c = mysql.get_db().cursor()
#     c.execute("SELECT * FROM productnames2")
#     names = c.fetchall()
#     conn.commit()
    

#     if names:
#         pass

#     namelist = []

#     for count, name in enumerate(names):
#         newname = str(name)
#         size = len(newname)
#         newname = newname[1:]
#         mod_string = newname[:size - 3]
#         namelist.append(str(mod_string))
    
    
#     query = ''
#     newquery = ''
#     if  len(namelist) > 0:
#         query = "SELECT * FROM reviews2 WHERE "
#         productquery = " product=("
#         productquery2 = ")"

        

#         if len(namelist) == 1:
#             newquery = productquery  + namelist[0] + productquery2

#         elif len(namelist) > 1:
#             for i in range(0,len(namelist)):
#               newquery += productquery  + namelist[i] + productquery2 
#               if i+1 != len(namelist):
#                 newquery += "OR"


        
    
#     finalquery = query + newquery
      
#     c.execute(finalquery)

#     reviews = list(c.fetchall())
    
#     conn.commit()
#     mainlist = []

#     totalreviews = len(reviews)


#     ratinglist = []
#     poscounter = 0
#     negcounter = 0
#     for i in reviews:
#        rating = str(i[3])
#        floatrating = float(rating.replace(' out of 5 stars',''))
#        ratinglist.append(floatrating)
#        sentiment = str(i[4])
#        sentiment = ast.literal_eval(sentiment)
#        if float(sentiment['neg']) > float(sentiment['pos']):
#             negcounter = negcounter + 1
#        else:
#             poscounter = poscounter + 1
        
#     averagerating = str(sum(ratinglist)/(totalreviews))

#     posComments = 0
#     #for index, element in enumerate(index11()):
#     #    posComments += element["positivecomments"]
#         #print (posComments)

#     negComments = 0
#     #for index, element in enumerate(index12()):
#     #    negComments += element["negativecomments"]
#         #print (negComments)

#     mainlist.append(str(totalreviews))
#     mainlist.append(poscounter)
#     mainlist.append(negcounter)
#     mainlist.append(averagerating)
#     mainlist.append(posComments)
#     mainlist.append(negComments)

#     c.close()

    
#     return mainlist
#    except:
#     return 'test'








#when the products are selected it outputs the names to the server and stores it in SQL
@app.route("/test2",methods = ['GET', 'POST'])
def index2():
    content_type = request.headers.get('Content-Type')
    
    if (content_type == 'application/json'):
        data = request.get_json(force=True, cache=True)
        return outputtojson(data)
        
    else:
        return 'data1'












#Outputs the data for all the names of the products stored in the database 
@app.route("/test3",methods = ['GET', 'POST'])
def index3():
   try:
    conn = mysql.connect()
    conn.autocommit(True)
    c = mysql.get_db().cursor()
    # c = conn.cursor(buffered=True)
    c.execute("SELECT * FROM productnames")
    productnames = c.fetchall()
    conn.commit()
    c.close()
    if productnames:
        pass
    mainlist = []
    for i in productnames:   
       mainlist.append(i[0])
    
    return mainlist
   except:
    return 'test'

    







#returns the data needed for the average rating graph
@app.route("/test4")
def index4():



   try:
    conn = mysql.connect()
    conn.autocommit(True)
    # c = conn.cursor(buffered=True)
    c = mysql.get_db().cursor()
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
              

    print(namelist)      
    print(vinelist)
    print(marketplacelist)
    #print(newquery)
    finalquery = query + newquery
    print(newquery)
    print(finalquery)  
    c.execute(finalquery)

    reviews = list(c.fetchall())
    #print(reviews)
    ratingdict = {}
    ratingdata = []


    for i in reviews:
        date = str(i[2])
        rating = str(i[4])
        product = str(i[0])
        d = datetime.datetime.strptime(date, '%d %B %Y')
        formatteddate = (d.strftime("%B %Y"))
        floatrating = float(rating.replace(' out of 5 stars',''))
        counter = 0
        ratingdict = {'product': product, 'rating': floatrating, 'date': formatteddate}
        ratingdata.append(ratingdict)
    
    print(ratingdata)

    results = {}

    for entry in ratingdata:
        product = entry['product']
        rating = entry['rating']
        date = datetime.datetime.strptime(entry['date'], '%B %Y')
        month_year = date.strftime("%B %Y")

        if month_year not in results:
            results[month_year] = {}

        if product not in results[month_year]:
            results[month_year][product] = []

        results[month_year][product].append(rating)

    averages = []

    for month_year, product_ratings in results.items():
        monthly_averages = {'name': month_year}
        for product, ratings in product_ratings.items():
            monthly_averages[product] = f"{sum(ratings) / len(ratings):.1f}"
        averages.append(monthly_averages)

    averages.sort(key=lambda x: datetime.datetime.strptime(x['name'], '%B %Y'))
    print(averages)
    # conn.commit()


    # productlist = []
    # totalreviews = len(reviews)
    # ratinglist = []
    


    # for i in reviews:
    #    rating = str(i[4])
    #    floatrating = float(rating.replace(' out of 5 stars',''))
    #    ratinglist.append(floatrating)
    #    sentiment = str(i[5])
    #    sentiment = ast.literal_eval(sentiment)
    #    if float(sentiment['neg']) > float(sentiment['pos']):
    #         negcounter = negcounter + 1
    #    else:
    #         poscounter = poscounter + 1
        
    # averagerating = str(sum(ratinglist)/(totalreviews))

    # posComments = 0
    

    # negComments = 0
    

    # mainlist.append(str(totalreviews))
    # mainlist.append(poscounter)
    # mainlist.append(negcounter)
    # mainlist.append(averagerating)
    # mainlist.append(posComments)
    # mainlist.append(negComments)

    c.close()

    
    return averages
   except:
    return 'test'
    
 
   




@app.route("/test9", methods = ['GET', 'POST'])
def test9():
    content_type = request.headers.get('Content-Type')
    
    if (content_type == 'application/json'):

        data = request.get_json(force=True, cache=True)
        print(data[0])
        commandlist = []
        for i in data:
           commandlist.append(str(i))
        print('test')
        return removeproduct(commandlist)
        
        
    else:
        return 'data1'



#Outputs the data in the form compatible with the compare feature 
@app.route("/test10",methods = ['GET', 'POST'])
def index10():
   try:
    conn = mysql.connect()
    conn.autocommit(True)
    # c = conn.cursor(buffered=True)
    c = mysql.get_db().cursor()
    c.execute("SELECT * FROM productnames")
    names = c.fetchall()
    conn.commit()
    

    if names:
        pass

    
    namelist = []

    for count, name in enumerate(names):
        newname = str(name)
        size = len(newname)
        newname = newname[1:]
        mod_string = newname[:size - 3]
        namelist.append(str(mod_string))
        print(namelist)
        
    
    
    query = ''
    newquery = ''
    mainlist = []
    mainsublist = {}
    if  len(namelist) > 0:
        query = "SELECT * FROM reviews1 WHERE "
        productquery = " product=("
        productquery2 = ")"

        

        if len(namelist) == 1:
            newquery = productquery  + namelist[0] + productquery2

        elif len(namelist) > 1:
            for i in range(0,len(namelist)):
                newquery = ''  
                newquery += productquery  + namelist[i] + productquery2 
                print(newquery)
               
                #if i+1 != len(namelist):
                    #newquery += "OR"
                finalquery = query + newquery
      
                c.execute(finalquery)

                reviews = list(c.fetchall())
                
                conn.commit()
                
                totalreviews = len(reviews)


                ratinglist = []
                poscounter = 0
                negcounter = 0
                for j in reviews:
                    rating = str(j[3])
                    floatrating = float(rating.replace(' out of 5 stars',''))
                    ratinglist.append(floatrating)
                    sentiment = str(j[4])
                    sentiment = ast.literal_eval(sentiment)
                    if float(sentiment['neg']) > float(sentiment['pos']):
                            negcounter = negcounter + 1
                    else:
                            poscounter = poscounter + 1
                
                
                    
                averagerating = str(sum(ratinglist)/(totalreviews))

                
                #mainlist.append(str(totalreviews))
                #mainlist.append(poscounter)
                #mainlist.append(negcounter)
                #mainlist.append(averagerating)
                #mainlist.append(mod_string)

                mainsublist = {'id': (i+1), 'name': (namelist[i]), 'totalrevs':totalreviews, 'posC': poscounter, 'negC': negcounter, 'avgRating':averagerating}
                print(mainsublist)
                mainlist.append(mainsublist)
                            


        
    
    

    c.close()

    
    return mainlist
   except:
    return 'test'


   
    
   






#KEYWORD ANALYSIS


#When the products are selected it forms a table for the keywords
@app.route("/test5",methods = ['GET', 'POST'])
def index5():
    content_type = request.headers.get('Content-Type')
    
    if (content_type == 'application/json'):
        data = request.get_json(force=True, cache=True)
        
        return keywordtable(data)
        
    else:
        return 'data1'

#When the products are selected it forms a table for the keywords
@app.route("/test15",methods = ['GET', 'POST'])
def index15():
    content_type = request.headers.get('Content-Type')
    
    if (content_type == 'application/json'):
        data = request.get_json(force=True, cache=True)
        print(allreviewtable(data))
        return allreviewtable(data)
        
        
    else:
        return 'data1'







#Outputs the data of the keywords to the server
@app.route("/test6",methods = ['GET', 'POST'])
def index6():
   try:
    conn = mysql.connect()
    conn.autocommit(True)
    c = mysql.get_db().cursor()
    # c = conn.cursor(buffered=True)
    c.execute("SELECT * FROM keywords")
    productnames = c.fetchall()
    conn.commit()
    
    if productnames:
        pass
    mainlist = []
    mainlist1= {}
    idCounter = 1
    for i in productnames:   
       sentiment = str(i[2])
       #print(i[2])
       sentiment = ast.literal_eval(sentiment)
       sentiment["pos"] = sentiment["pos"]*100
       sentiment["neg"] = sentiment["neg"]*100
       mainlist1 = {'id':idCounter, 'keyword':(i[0]),'mentions':int(i[1]),'positive':sentiment['pos'],'negative':sentiment['neg'],'averagerating':i[3],}
       print(mainlist1)
       mainlist.append(mainlist1)
       mainlist1 ={}
       idCounter += 1
       
    c.execute("SELECT * FROM keywordnames")
    sortvalue = str(c.fetchall())
    conn.commit()
    print(sortvalue)
    newvalue = sortvalue.replace(',),)','')
    newvalue1 = newvalue.replace('((','')
    print(str(newvalue1))

    if str(newvalue1) == "'Keyword'":
        print('testtt')
        mainlist = sorted(mainlist, key=lambda d: d['keyword']) 
    
    if str(newvalue1) == "'Positive'":
        print('testtt')
        mainlist = sorted(mainlist, key=lambda d: d['positive'], reverse=True) 

    if str(newvalue1) == "'Negative'":
        print('testtt')
        mainlist = sorted(mainlist, key=lambda d: d['negative'], reverse=True) 
    
    if str(newvalue1) == "'Records'":
        print('testtt')
        mainlist = sorted(mainlist, key=lambda d: d['mentions'], reverse=True)
    
    if str(newvalue1) == "'Average Rating'":
        print('testtt')
        mainlist = sorted(mainlist, key=lambda d: d['averagerating'], reverse=True) 
    c.close
    

    return mainlist
   except:
    return 'test'










#When a keyword is selected it adds it to the table
@app.route("/test7", methods = ['GET', 'POST'])
def test7():
    content_type = request.headers.get('Content-Type')
    conn = mysql.connect()
    conn.autocommit(True)
    c = mysql.get_db().cursor()
    
    if (content_type == 'application/json'):

        data = request.get_json(force=True, cache=True)

        c.execute("SELECT * FROM productnames2")

        productnames = c.fetchall()
        conn.commit()

        c.close()

        klist = []
        plist = []

        klist.append(data['search'])
    
        for i in productnames:
            plist.append(i[0])
            print(i)

        return keywordtable1(plist,klist)
        
        
        
        
    else:
        return 'data1'



@app.route("/test8", methods = ['GET', 'POST'])
def test8():
    content_type = request.headers.get('Content-Type')
    
    if (content_type == 'application/json'):

        data = request.get_json(force=True, cache=True)
        print(data)
        commandlist = []
        commandlist.append(str(data))
        print('test')


        return outputkeywordsort(commandlist)
        
        
        
        
    else:
        return 'data1'

@app.route("/test11")
def index11():



   try:
    conn = mysql.connect()
    conn.autocommit(True)
    # c = conn.cursor(buffered=True)
    c = mysql.get_db().cursor()
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
              

    print(namelist)      
    print(vinelist)
    print(marketplacelist)
    #print(newquery)
    finalquery = query + newquery
    print(newquery)
    print(finalquery)  
    c.execute(finalquery)

    reviews = list(c.fetchall())
    #print(reviews)
    positivedict = {}
    positivedata = []
    productnames = []
    

    for i in reviews:
        date = str(i[2])
        rating = str(i[4])
        product = str(i[0])
        d = datetime.datetime.strptime(date, '%d %B %Y')
        formatteddate = (d.strftime("%B %Y"))
        sentiment = str(i[5])
        sentiment = ast.literal_eval(sentiment)
        counter = 0
        
        
        if float(sentiment['neg']) < float(sentiment['pos']):

            counter = counter + 1
        
        floatrating = float(rating.replace(' out of 5 stars',''))
        positivedict = {'product': product, 'sentiment': counter, 'date': formatteddate}
        positivedata.append(positivedict)
    

    #print(positivedata)


    def count_monthly_mentions(data):
        count = defaultdict(lambda: defaultdict(int))
        for item in data:
            date = datetime.datetime.strptime(item[2], '%d %B %Y')
            count[item[0]][date.strftime('%B %Y')] += 1
        return dict(count)

    
    result = count_monthly_mentions(reviews)
    #print (result)
    results_list = []
    for product, months in result.items():
        for month, count in months.items():
            results_list.append({"Product": product, "Month": month, "Count": count})

    print(results_list)

    def avg_positive_comments(monthly_product_count, positive_comments):
        avg_pos_comments = []
        for count in monthly_product_count:
            product = count['Product']
            month = count['Month']
            total_count = count['Count']
            pos_comments = 0
            for comment in positive_comments:
                if comment['product'] == product and month in comment['date']:
                    pos_comments += comment['sentiment']
            avg_pos_comments.append({product: pos_comments/total_count if total_count != 0 else 0, 'date': month})
        return sorted(avg_pos_comments, key=lambda x: x['date'])

    finaloutput = (avg_positive_comments(results_list, positivedata))
    #finaloutput = avg_positive_comments(results_list, positivedata)

#    print(result)

    # for entry in positivedata:
    #     product = entry['product']
    #     rating = entry['rating']
    #     date = datetime.datetime.strptime(entry['date'], '%B %Y')
    #     month_year = date.strftime("%B %Y")

    #     if month_year not in results:
    #         results[month_year] = {}

    #     if product not in results[month_year]:
    #         results[month_year][product] = []

    #     results[month_year][product].append(rating)

    # averages = []

    # for month_year, product_ratings in results.items():
    #     monthly_averages = {'name': month_year}
    #     for product, ratings in product_ratings.items():
    #         monthly_averages[product] = f"{sum(ratings) / len(ratings):.1f}"
    #     averages.append(monthly_averages)

    # averages.sort(key=lambda x: datetime.datetime.strptime(x['name'], '%B %Y'))
    # print(averages)
    # conn.commit()


    # productlist = []
    # totalreviews = len(reviews)
    # ratinglist = []
    


    # for i in reviews:
    #    rating = str(i[4])
    #    floatrating = float(rating.replace(' out of 5 stars',''))
    #    ratinglist.append(floatrating)
    #    sentiment = str(i[5])
    #    sentiment = ast.literal_eval(sentiment)
    #    if float(sentiment['neg']) > float(sentiment['pos']):
    #         negcounter = negcounter + 1
    #    else:
    #         poscounter = poscounter + 1
        
    # averagerating = str(sum(ratinglist)/(totalreviews))

    # posComments = 0
    

    # negComments = 0
    

    # mainlist.append(str(totalreviews))
    # mainlist.append(poscounter)
    # mainlist.append(negcounter)
    # mainlist.append(averagerating)
    # mainlist.append(posComments)
    # mainlist.append(negComments)

    c.close()

    
    return finaloutput
   except:
    return 'test'



@app.route("/avgnegativegraph")
def avgnegativegraph():



   try:
    conn = mysql.connect()
    conn.autocommit(True)
    # c = conn.cursor(buffered=True)
    c = mysql.get_db().cursor()
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
              

    print(namelist)      
    print(vinelist)
    print(marketplacelist)
    #print(newquery)
    finalquery = query + newquery
    print(newquery)
    print(finalquery)  
    c.execute(finalquery)

    reviews = list(c.fetchall())
    #print(reviews)
    positivedict = {}
    positivedata = []
    productnames = []
    

    for i in reviews:
        date = str(i[2])
        rating = str(i[4])
        product = str(i[0])
        d = datetime.datetime.strptime(date, '%d %B %Y')
        formatteddate = (d.strftime("%B %Y"))
        sentiment = str(i[5])
        sentiment = ast.literal_eval(sentiment)
        counter = 0
        
        
        if float(sentiment['neg']) > float(sentiment['pos']):

            counter = counter + 1
        
        floatrating = float(rating.replace(' out of 5 stars',''))
        positivedict = {'product': product, 'sentiment': counter, 'date': formatteddate}
        positivedata.append(positivedict)
    

    #print(positivedata)


    def count_monthly_mentions(data):
        count = defaultdict(lambda: defaultdict(int))
        for item in data:
            date = datetime.datetime.strptime(item[2], '%d %B %Y')
            count[item[0]][date.strftime('%B %Y')] += 1
        return dict(count)

    
    result = count_monthly_mentions(reviews)
    #print (result)
    results_list = []
    for product, months in result.items():
        for month, count in months.items():
            results_list.append({"Product": product, "Month": month, "Count": count})

    print(results_list)

    def avg_positive_comments(monthly_product_count, positive_comments):
        avg_pos_comments = []
        for count in monthly_product_count:
            product = count['Product']
            month = count['Month']
            total_count = count['Count']
            pos_comments = 0
            for comment in positive_comments:
                if comment['product'] == product and month in comment['date']:
                    pos_comments += comment['sentiment']
            avg_pos_comments.append({product: pos_comments/total_count if total_count != 0 else 0, 'date': month})
        return sorted(avg_pos_comments, key=lambda x: x['date'])

    finaloutput = (avg_positive_comments(results_list, positivedata))
    #finaloutput = avg_positive_comments(results_list, positivedata)

#    print(result)

    # for entry in positivedata:
    #     product = entry['product']
    #     rating = entry['rating']
    #     date = datetime.datetime.strptime(entry['date'], '%B %Y')
    #     month_year = date.strftime("%B %Y")

    #     if month_year not in results:
    #         results[month_year] = {}

    #     if product not in results[month_year]:
    #         results[month_year][product] = []

    #     results[month_year][product].append(rating)

    # averages = []

    # for month_year, product_ratings in results.items():
    #     monthly_averages = {'name': month_year}
    #     for product, ratings in product_ratings.items():
    #         monthly_averages[product] = f"{sum(ratings) / len(ratings):.1f}"
    #     averages.append(monthly_averages)

    # averages.sort(key=lambda x: datetime.datetime.strptime(x['name'], '%B %Y'))
    # print(averages)
    # conn.commit()


    # productlist = []
    # totalreviews = len(reviews)
    # ratinglist = []
    


    # for i in reviews:
    #    rating = str(i[4])
    #    floatrating = float(rating.replace(' out of 5 stars',''))
    #    ratinglist.append(floatrating)
    #    sentiment = str(i[5])
    #    sentiment = ast.literal_eval(sentiment)
    #    if float(sentiment['neg']) > float(sentiment['pos']):
    #         negcounter = negcounter + 1
    #    else:
    #         poscounter = poscounter + 1
        
    # averagerating = str(sum(ratinglist)/(totalreviews))

    # posComments = 0
    

    # negComments = 0
    

    # mainlist.append(str(totalreviews))
    # mainlist.append(poscounter)
    # mainlist.append(negcounter)
    # mainlist.append(averagerating)
    # mainlist.append(posComments)
    # mainlist.append(negComments)

    c.close()

    
    return finaloutput
   except:
    return 'test'





@app.route("/vine", methods = ['GET', 'POST'])
def process_vine():

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json') and (request.method == 'POST'):
        data = request.get_json(force=True, cache=True)
        print(data[0])
       

        return vinefilter(data)

    else:
        return 'data1'


@app.route("/marketplace", methods = ['GET', 'POST'])
def process_marketplace():

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json') and (request.method == 'POST'):
        data = request.get_json(force=True, cache=True)
        print(data[0])
       

        return marketplacefilter(data)

    else:
        return 'data1'

@app.route("/dashboardfiltered")
def dashboardFilter():

   try:
    conn = mysql.connect()
    conn.autocommit(True)
    # c = conn.cursor(buffered=True)
    c = mysql.get_db().cursor()
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
              

    print(namelist)      
    print(vinelist)
    print(marketplacelist)
    #print(newquery)
    finalquery = query + newquery
    print(newquery)
    print(finalquery)  
    c.execute(finalquery)

    reviews = list(c.fetchall())
    print(reviews)
    conn.commit()
    mainlist = []

    totalreviews = len(reviews)


    ratinglist = []
    poscounter = 0
    negcounter = 0
    for i in reviews:
       rating = str(i[4])
       floatrating = float(rating.replace(' out of 5 stars',''))
       ratinglist.append(floatrating)
       sentiment = str(i[5])
       sentiment = ast.literal_eval(sentiment)
       if float(sentiment['neg']) > float(sentiment['pos']):
            negcounter = negcounter + 1
       else:
            poscounter = poscounter + 1
        
    averagerating = str(sum(ratinglist)/(totalreviews))

    posComments = 0
    

    negComments = 0
    

    mainlist.append(str(totalreviews))
    mainlist.append(poscounter)
    mainlist.append(negcounter)
    mainlist.append(averagerating)
    mainlist.append(posComments)
    mainlist.append(negComments)

    c.close()

    
    return mainlist
   except:
    return 'test'


@app.route("/vinecounter")
def vinecounter():

   try:
    conn = mysql.connect()
    conn.autocommit(True)
    # c = conn.cursor(buffered=True)
    c = mysql.get_db().cursor()
    c.execute("SELECT * FROM productnames2")
    names = c.fetchall()
    conn.commit()
    c.execute("SELECT * FROM marketplaces")
    marketplaces = c.fetchall()
    conn.commit()


    if names:
        pass

    namelist = []

    for count, name in enumerate(names):
        newname = str(name)
        size = len(newname)
        newname = newname[1:]
        mod_string = newname[:size - 3]
        namelist.append(str(mod_string))

    marketplacelist = []

    for count, market in enumerate(marketplaces):
        newmarket = str(market)
        size1 = len(newmarket)
        newmarket = newmarket[1:]
        mod_string1 = newmarket[:size1 - 3]
        marketplacelist.append(str(mod_string1))


    query = ''
    newquery = ''
    if  len(namelist) > 0:
        query = "SELECT * FROM reviews1 WHERE "
        productquery = " product=("
        marketplacequery = " marketplace=("
        andquery = 'AND'
        productquery2 = ")"



        if len(namelist) == 1:
            newquery = productquery  + namelist[0] + productquery2

        elif len(namelist) > 1:
            for i in range(0,len(namelist)):
              newquery += productquery  + namelist[i] + productquery2 
              if i+1 != len(namelist):
                newquery += "OR"




    finalquery = query + newquery

    c.execute(finalquery)

    reviews = list(c.fetchall())

    conn.commit()
    mainlist = []

    totalreviews = len(reviews)


    ratinglist = []
    poscounter = 0
    negcounter = 0
    for i in reviews:
       rating = str(i[3])
       floatrating = float(rating.replace(' out of 5 stars',''))
       ratinglist.append(floatrating)
       sentiment = str(i[4])
       sentiment = ast.literal_eval(sentiment)
       if float(sentiment['neg']) > float(sentiment['pos']):
            negcounter = negcounter + 1
       else:
            poscounter = poscounter + 1

    averagerating = str(sum(ratinglist)/(totalreviews))

    mainlist.append(str(totalreviews))
    mainlist.append(poscounter)
    mainlist.append(negcounter)
    mainlist.append(averagerating)
    c.close()


    return mainlist
   except:
    return 'test'





#COPY IN

@app.route("/individualkeywordtable", methods = ['GET', 'POST'])
def individualkeywordtable():

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json') and (request.method == 'POST'):
        data = request.get_json(force=True, cache=True)
        print(data[0])
        keyword = 'wipes'

        return individual_keyword(keyword)

    else:
        return 'data1'


@app.route("/mainindividualkeywordtable")
def mainindividualkeywordtable():
        conn = mysql.connect()
        conn.autocommit(True)
        c = mysql.get_db().cursor()
        c.execute('SELECT * FROM keyword_specific')
        keywords = c.fetchall()
        conn.commit()
        return jsonify(keywords)



@app.route("/mainindividualkeywordtablepositivecomments")
def mainindividualkeywordtablepositivecomments():
        conn = mysql.connect()
        conn.autocommit(True)
        c = mysql.get_db().cursor()
        c.execute('SELECT * FROM keyword_specific')
        keywords = c.fetchall()
        conn.commit()
        keywords1 = jsonify(keywords)
        def avg_pos_reviews(data):
            product_reviews = {}
            for review in data:
                product = review[0]
                date_str = review[2]
                sentiment = ast.literal_eval(review[5])
                date = datetime.strptime(date_str, "%d %B %Y")
                month_year = f"{date.strftime('%B')} {date.year}"
                
                if product not in product_reviews:
                    product_reviews[product] = {}
                if month_year not in product_reviews[product]:
                    product_reviews[product][month_year] = {"total": 0, "positive": 0}
                
                product_reviews[product][month_year]["total"] += 1
                if sentiment["pos"] > sentiment["neg"]:
                    product_reviews[product][month_year]["positive"] += 1
            
            avg_reviews = []
            for product, product_data in product_reviews.items():
                for month_year, review_data in product_data.items():
                    avg_reviews.append({product: review_data["positive"] / review_data["total"],"date": month_year})
            
            avg_reviews = sorted(avg_reviews, key=lambda x: datetime.strptime(x['date'], "%B %Y"))
            return avg_reviews
        
        return avg_pos_reviews(keywords)



@app.route("/mainindividualkeywordtablenegativecomments")
def mainindividualkeywordtablenegativecomments():
        conn = mysql.connect()
        conn.autocommit(True)
        c = mysql.get_db().cursor()
        c.execute('SELECT * FROM keyword_specific')
        keywords = c.fetchall()
        conn.commit()
        keywords1 = jsonify(keywords)
        def avg_pos_reviews(data):
            product_reviews = {}
            for review in data:
                product = review[0]
                date_str = review[2]
                sentiment = ast.literal_eval(review[5])
                date = datetime.strptime(date_str, "%d %B %Y")
                month_year = f"{date.strftime('%B')} {date.year}"
                
                if product not in product_reviews:
                    product_reviews[product] = {}
                if month_year not in product_reviews[product]:
                    product_reviews[product][month_year] = {"total": 0, "positive": 0}
                
                product_reviews[product][month_year]["total"] += 1
                if sentiment["pos"] < sentiment["neg"]:
                    product_reviews[product][month_year]["positive"] += 1
            
            avg_reviews = []
            for product, product_data in product_reviews.items():
                for month_year, review_data in product_data.items():
                    avg_reviews.append({product: review_data["positive"] / review_data["total"],"date": month_year})
            
            avg_reviews = sorted(avg_reviews, key=lambda x: datetime.strptime(x['date'], "%B %Y"))
            return avg_reviews
        
        return avg_pos_reviews(keywords)


@app.route("/mainindividualkeywordtabletotalcomments")
def mainindividualkeywordtabletotalcomments():
        conn = mysql.connect()
        conn.autocommit(True)
        c = mysql.get_db().cursor()
        c.execute('SELECT * FROM keyword_specific')
        keywords = c.fetchall()
        conn.commit()
        def transform_date(date_str):
            date_obj = datetime.strptime(date_str, '%d %B %Y')
            return date_obj.strftime("%B %Y")
        review_count = defaultdict(int)
        for product, review, date, country, rating, sentiment, verified_purchase in keywords:
            date = transform_date(date)
            review_count[(product, date)] += 1
            
        sorted_review_count = sorted(review_count.items(), key=lambda x: x[0][1])

        result = [{product: count, "date": date} for (product, date), count in sorted_review_count]
        
        return result


@app.route("/dateaverages")
def dateaverages():

   try:
    conn = mysql.connect()
    conn.autocommit(True)
    # c = conn.cursor(buffered=True)
    c = mysql.get_db().cursor()
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
              

    print(namelist)      
    print(vinelist)
    print(marketplacelist)
    #print(newquery)
    finalquery = query + newquery
    print(newquery)
    print(finalquery)  
    c.execute(finalquery)

    reviews = list(c.fetchall())
    print(reviews)
    conn.commit()
    def average_rating(data, num_days=7, num_months=6, num_years=1):
        now = datetime.now()
        ratings = {}
        for duration, num_units in zip(['7-day', '6-month', '1-year'], [num_days, num_months * 30, num_years * 365]):
            ratings[duration] = sum(float(item[4]) for item in data if (now - datetime.strptime(item[2], '%d %B %Y')).days <= num_units) / len([item[4] for item in data if (now - datetime.strptime(item[2], '%d %B %Y')).days <= num_units]) if [item[4] for item in data if (now - datetime.strptime(item[2], '%d %B %Y')).days <= num_units] else None
        return ratings

    def recommend_product(reviews):
        positive_reviews = [review for review in reviews if float(ast.literal_eval(review[5])["compound"]) > 0]
        positive_reviews = sorted(positive_reviews, key=itemgetter(4), reverse=True)
        if positive_reviews:
            return positive_reviews[0][0]
        else:
            return None

    recommended_product = recommend_product(reviews)
    if recommended_product:
        print(f"The recommended product is: {recommended_product}")
        
    else:
        print("No product can be recommended as there are no positive reviews")

    c.close()

    mainlist = []
    mainlist.append(average_rating(reviews))
    mainlist.append(recommended_product)
    return jsonify(mainlist)
   except:
    return 'test'


@app.route("/volumegraph")
def volumegraph():

   try:
    conn = mysql.connect()
    conn.autocommit(True)
    # c = conn.cursor(buffered=True)
    c = mysql.get_db().cursor()
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
              

    print(namelist)      
    print(vinelist)
    print(marketplacelist)
    #print(newquery)
    finalquery = query + newquery
    print(newquery)
    print(finalquery)  
    c.execute(finalquery)

    reviews = c.fetchall()
    # print(reviews)
    conn.commit()
    def transform_date(date_str):
        date_obj = datetime.strptime(date_str, '%d %B %Y')
        return date_obj.strftime("%B %Y")
    review_count = defaultdict(int)
    for product, review, date, country, rating, sentiment, verified_purchase in reviews:
        date = transform_date(date)
        review_count[(product, date)] += 1
        
    sorted_review_count = sorted(review_count.items(), key=lambda x: x[0][1])

    result = [{product: count, "date": date} for (product, date), count in sorted_review_count]

    c.close()

    
    return result
   except:
    return 'test'


if __name__ == "__main__":
    app.run(debug=True, threaded = True, use_reloader=True)
    server = Server(app.wsgi_app)
    server.serve(host = '127.0.0.1',port=5000)
