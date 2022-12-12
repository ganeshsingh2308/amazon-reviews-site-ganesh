
import json
import mysql.connector
import ast
conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 



def removeproduct(commandlist):
   conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 
   print(commandlist)
   

   c = conn.cursor(buffered=True)
   if  len(commandlist) > 0:
      query1 = "DELETE FROM productnames WHERE "
      query2 = "DELETE FROM reviews1 WHERE "
      query3 = "DELETE FROM amazonlink WHERE "
      productquery = " product=('"
      productquery2 = "')"

        

      if len(commandlist) == 1:
         newquery = productquery  + commandlist[0] + productquery2

      elif len(commandlist) > 1:
         for i in range(0,len(commandlist)):
            newquery += productquery  + commandlist[i] + productquery2 
            if i+1 != len(commandlist):
               newquery += "OR"


        
    
   finalquery = query1 + newquery
   finalquery1 = query2 + newquery
   finalquery2 = query3 + newquery

   c.execute(finalquery)
   conn.commit()
   c.execute(finalquery1)
   conn.commit()
   c.execute(finalquery2)
   
   conn.commit()
   conn.close()
   c.close()
      
    
   return 'test'



