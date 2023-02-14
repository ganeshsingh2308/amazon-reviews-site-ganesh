

import mysql.connector
conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 

def filter_reviews():
    c = conn.cursor()
    c.execute("SELECT * FROM productnames2")
    products = c.fetchall()
    conn.commit()
    result1 = []
    result2 = []
    result3 = []
    for row in products:
        row_values = [str(val) for val in row] # convert each value
        row_string = " ".join(row_values) # join values as a string with a space separator
        result1.append(row_string)
    c.execute("SELECT * FROM marketplace")
    markets = c.fetchall()
    conn.commit()
    for row in markets:
        row_values = [str(val) for val in row] # convert each value
        row_string = " ".join(row_values) # join values as a string with a space separator
        result2.append(row_string)
    c.execute("SELECT * FROM vine")
    product_types = c.fetchall()
    conn.commit()
    for row in product_types:
        row_values = [str(val) for val in row] # convert each value
        row_string = " ".join(row_values) # join values as a string with a space separator
        result3.append(row_string)


    query = "SELECT * FROM reviews2 WHERE product IN ({}) AND marketplace IN ({}) AND vine IN ({});".format(
        ", ".join(["'{}'".format(p) for p in result1]), 
        ", ".join(["'{}'".format(m) for m in result2]), 
        ", ".join(["'{}'".format(t) for t in result3])
    )

    c.execute(query)

    reviews = c.fetchall()
    conn.commit()

    print(reviews)

    conn.close()
    c.close()
    return reviews

