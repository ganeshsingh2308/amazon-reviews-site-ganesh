
import json
import mysql.connector
import ast
conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 



def vinefilter(data):
    conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 
    c = conn.cursor(buffered=True)
    
    c.execute("DELETE FROM vine")
    conn.commit()
    
    for i in range(0, len(data)):
            
        
        
        c.execute("INSERT INTO vine (filter) VALUES (%s)",([data[i]]))
        conn.commit()
    c.stored_results()
    c.close()
    conn.close()
      
    
    return 'test'


