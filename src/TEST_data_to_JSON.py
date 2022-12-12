
import json
import mysql.connector
import ast
conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 



def outputtojson(commandlist):
   conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 
   

   c = conn.cursor(buffered=True)
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
   commandlistnew.append(commandlist)


   
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
   conn.close()
   c.close()
      
    
   return 'test'



