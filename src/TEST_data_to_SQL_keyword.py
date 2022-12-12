
import json
import mysql.connector
import ast
conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 



def outputkeywordsort(commandlist):
   conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 
   

   c = conn.cursor(buffered=True)
   c.execute("SELECT * FROM keywordnames")
   names = c.fetchall()
   print(names)
   lengthofnames = len(names)

   if lengthofnames > 0:
      c.execute("DELETE FROM keywordnames")

 
   c.execute("INSERT INTO keywordnames (keyword) VALUES (%s)",(commandlist))
   c.stored_results()
   conn.commit()
   conn.close()
   c.close()
      
    
   return 'test'



