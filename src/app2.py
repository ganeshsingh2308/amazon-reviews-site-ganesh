from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_cors import CORS

from flaskext.mysql import MySQL
import mysql.connector
import ast
from webscraper_FINAL_MYSQL import scrape_amazon
from TEST_data_to_JSON import outputtojson
from TEST_data_to_REMOVEBUTTON import removeproduct
from TEST_data_to_SQL_keyword import outputkeywordsort
from table1FINAL_MYSQL1 import keywordtable
from table1FINAL_MYSQL2 import keywordtable1
from livereload import Server
import time
import json






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
        c.execute("SELECT * FROM amazonlink")
        names = c.fetchall()
        conn.commit()

        for i in names:
            newname = str(i).replace("('","")
            newname1 = newname.replace("',)","")

            if data['search'] == str(newname1):
                returnstate = "link already here"

        if str(data['search'])[0:18] != 'https://www.amazon':
            returnstate = 'Wrong Link'

        

        if returnstate == '':
            scrape_amazon(data['search'])
        

        print(jsonify(returnstate))
        state1 = jsonify({'name':returnstate})
        

    
        return jsonify(returnstate)
        
    else:
        return 'data1'





#When the combination of products is selected then it will output a list of all the data for Number of reviews, average rating and positive/negative reviews
@app.route("/test")
def index():

   try:
    conn = mysql.connect()
    conn.autocommit(True)
    # c = conn.cursor(buffered=True)
    c = mysql.get_db().cursor()
    c.execute("SELECT * FROM productnames2")
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
    
    
    query = ''
    newquery = ''
    if  len(namelist) > 0:
        query = "SELECT * FROM reviews1 WHERE "
        productquery = " product=("
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
    c = mysql.get_db().cursor()
    # c = conn.cursor(buffered=True)
    c.execute("SELECT * FROM productnames2")
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
    
    
    query = ''
    newquery = ''
    if  len(namelist) > 0:
        query = "SELECT * FROM reviews1 WHERE "
        productquery = " product=("
        productquery2 = ")"

        

        if len(namelist) == 1:
            newquery = productquery  + namelist[0] + productquery2

        elif len(namelist) > 1:
            for i in range(0,len(namelist)):
              newquery += productquery  + namelist[i] + productquery2 
              if i+1 != len(namelist):
                newquery += "OR"


        
    
    finalquery = query + newquery

    conn = mysql.connect()
    conn.autocommit(True)
    c = mysql.get_db().cursor()
            
    c.execute(finalquery)

    productname = list(c.fetchall())
    
    conn.commit()
    ratingdict = {}
    ratinglist = []

    for i in productname:
        date = str(i[2])
        rating = str(i[3])
        # date1 = date.replace("Reviewed in the United Kingdom ", "")
        # date2 = date1[2::]
        # date3 = date2.replace('on ','')
        # date4 = date3[3::]
        # date4 = date4.replace(' ','')
        if date[23] == 'K':
            date1 = date.replace("Reviewed in the United Kingdom ", "")
            date2 = date1[2::]
            date3 = date2.replace('on ','')
            date4 = date3[3::]
            date4 = date4.replace(' ','')
        elif date[23] == 'S':
            date1 = date.replace("Reviewed in the United States", "")
            date2 = date1.replace('on ','')
            year = date2[-4:]
            month = []
            counter  = 0
            def convert(s):
               str1 = ""
               return(str1.join(s))

            for j in date2:
                counter = counter + 1
                month.append(j)
                if counter > 1 and j == ' ':
                   break   
            newmonth = convert(month)
            if newmonth[0] == ' ':
                newmonth1 = newmonth.replace(' ', '') 
                            
            totaldate = newmonth1 + year
            date4 = totaldate

        floatrating = float(rating.replace(' out of 5 stars',''))
        counter = 0
        for j in ratinglist:
            counter = counter + 1
            if j['date'] == date4:
                counter = counter - 1
                j['rating'].append(floatrating)
        if counter == len(ratinglist):
            floatratinglist = []
            floatratinglist.append(floatrating)
            ratingdict = {'date':date4,'rating':floatratinglist}
            ratinglist.append(ratingdict)
        
    for i in ratinglist:
        i['rating'] = sum(i['rating']) / len(i['rating'])
            
    
    c.close()
    def sort_vals(values):
            months = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
            return sorted(values, key = lambda x: [int(x['date'][-4:]),months[x['date'][:-4]]])
    
    return sort_vals(ratinglist)
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
    for i in productnames:   
       sentiment = str(i[2])
       sentiment = ast.literal_eval(sentiment)
       mainlist1 = {'keyword':i[0],'mentions':int(i[1]),'positive':sentiment['pos'],'negative':sentiment['neg'],'averagerating':i[3],}
       mainlist.append(mainlist1)
       mainlist1 ={}
       
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









if __name__ == "__main__":
    app.run(debug=True, threaded = True, use_reloader=True)
    server = Server(app.wsgi_app)
    server.serve(host = '127.0.0.1',port=5000)

