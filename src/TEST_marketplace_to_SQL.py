import json
import mysql.connector
import ast
conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 



def marketplacefilter(data):
    conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 
    c = conn.cursor(buffered=True)
    
    c.execute("DELETE FROM marketplace")
    conn.commit()
    
    for i in range(0, len(data)):
            
        
        
        c.execute("INSERT INTO marketplace (filter) VALUES (%s)",([data[i]]))
        conn.commit()
    c.stored_results()
    c.close()
    conn.close()
      
    
    return 'test'