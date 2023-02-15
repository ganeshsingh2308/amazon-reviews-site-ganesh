import mysql.connector
import json
from filterreviews import filter_reviews
conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 


def keywordsummary():
    conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 
    c = conn.cursor()
    c = conn.cursor()
    c.execute("SELECT * FROM keywords")
    keywords = c.fetchall()
    print(keywords)
    def generate_summary(input_list):
        # Separate the keywords based on their sentiment scores
        positive_keywords = []
        negative_keywords = []
        neutral_keywords = []
        for keyword, mentions, sentiment, _ in input_list:
            sentiment = eval(sentiment)
            if sentiment['compound'] > 0.2:
                positive_keywords.append((keyword, mentions))
            elif sentiment['compound'] < -0.2:
                negative_keywords.append((keyword, mentions))
            else:
                neutral_keywords.append((keyword, mentions))
        
        # Generate the summary paragraph
        summary = "The product has"
        if len(positive_keywords) == 0 and len(negative_keywords) == 0:
            summary += " no standout features."
        else:
            if len(positive_keywords) > 0:
                summary += " the following standout features:"
                for keyword, mentions in positive_keywords:
                    summary += f" {keyword} ({mentions} mentions),"
                summary = summary.rstrip(",") + "."
            if len(negative_keywords) > 0:
                summary += " The following features could be improved:"
                for keyword, mentions in negative_keywords:
                    summary += f" {keyword} ({mentions} mentions),"
                summary = summary.rstrip(",") + "."
        
        if len(neutral_keywords) > 0:
            summary += " In addition, the product has the following neutral features:"
            for keyword, mentions in neutral_keywords:
                summary += f" {keyword} ({mentions} mentions),"
            summary = summary.rstrip(",") + "."
        
        return summary

    

    conn.close()
    c.close()
    return generate_summary(keywords)

print(keywordtable1())