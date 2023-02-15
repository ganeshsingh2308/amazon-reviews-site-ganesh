
# import datetime

# monthly_product_count = [{'Product': 'Fellowes', 'Month': 'August 2022', 'Count': 2}, {'Product': 'Fellowes', 'Month': 'December 2022', 'Count': 1}, {'Product': 'Magicjell', 'Month': 'December 2022', 'Count': 1}]
# positive_comments = [{'product': 'Magicjell', 'positive comments': 0, 'date': 'December 2022'}, {'product': 'Fellowes', 'positive comments': 1, 'date': 'August 2022'}, {'product': 'Fellowes', 'positive comments': 1, 'date': 'December 2022'}]

# # def avg_positive_comments(monthly_product_count, positive_comments):
# #     avg_pos_comments = []
# #     for count in monthly_product_count:
# #         product = count['Product']
# #         month = count['Month']
# #         total_count = count['Count']
# #         pos_comments = 0
# #         for comment in positive_comments:
# #             if comment['product'] == product and month in comment['date']:
# #                 pos_comments += comment['positive comments']
# #         avg_pos_comments.append({
# #             'Product': product,
# #             'Month': month,
# #             'Average Positive Comments': pos_comments/total_count if total_count != 0 else 0
# #         })
# #     return sorted(avg_pos_comments, key=lambda x: datetime.datetime.strptime(x['Month'], '%B %Y'))

# # print(avg_positive_comments(monthly_product_count, positive_comments))

# def avg_positive_comments(monthly_product_count, positive_comments):
#     avg_pos_comments = []
#     for count in monthly_product_count:
#         product = count['Product']
#         month = count['Month']
#         total_count = count['Count']
#         pos_comments = 0
#         for comment in positive_comments:
#             if comment['product'] == product and month in comment['date']:
#                 pos_comments += comment['positive comments']
#         avg_pos_comments.append({product: pos_comments/total_count if total_count != 0 else 0, 'date': month})
#     return sorted(avg_pos_comments, key=lambda x: x['date'])

# print(avg_positive_comments(monthly_product_count, positive_comments))



# from nltk.metrics.distance import edit_distance

# def find_similar_keyword(reviews, keyword):
#     result = []
#     for product, review, *rest in reviews:
#         if keyword in review:
#             result.append((product, review, *rest))
#         else:
#             for word in review.split():
#                 if edit_distance(word.lower(), keyword.lower()) <= 2:
#                     result.append((product, review, *rest))
#                     break
#     return result

# reviews = [('Fellowes', 'good', '6 July 2022', 'United Kingdom', '4.0', "{'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.4404}", 'Verified Purchase'), 
#            ('Fellowes', 'Bought to clean finger grease from iPad touch screen. The wipes are almost dry when taken from the packet and whilst using two or three wipes does the job.', '24 April 2022', 'United Kingdom', '3.0', "{'neg': 0.0, 'neu': 0.956, 'pos': 0.044, 'compound': 0.4019}", 'Verified Purchase'), 
#            ('Fellowes', 'Came already dried out, and besides some idiot stuck a huge sticky label over the opening so you cannot reseal it after using.', '31 December 2022', 'United Kingdom', '1.0', "{'neg': 0.192, 'neu': 0.725, 'pos': 0.083, 'compound': -0.4588}", 'Verified Purchase'), 
#            ('Fellowes ', 'The size of the wipes are small the pack is handy for work or handbag as small packet. The wipes came practically dry with exception of the middle couple! Expensive screen clean!', '15 September 2022', 'United Kingdom', '1.0', "{'neg': 0.0, 'neu': 0.904, 'pos': 0.096, 'compound': 0.508}", 'Verified Purchase'), 
#            ('Fellowes', 'Arrived quickly and worked well', '2 January 2022', 'United Kingdom', '5.0', "{'neg': 0.0, 'neu': 0.656, 'pos': 0.344, 'compound': 0.2732}", 'Verified Purchase'), 
#            ('Fellowes', 'Bought these a while ago and still amazed by its price and functionality , highly recommend .', '3 November 2021', 'United Kingdom', '5.0', "{'neg': 0.0, 'neu': 0.715, 'pos': 0.285, 'compound': 0.7178}", 'Verified Purchase'), 
#            ('Fellowes', 'Good quality .. cleaned some button imprints off.', '6 December 2021', 'United Kingdom', '5.0', "{'neg': 0.0, 'neu': 0.707, 'pos': 0. 293, 'compound': 0.4404}", 'Verified Purchase')]

# keyword = "good"

# result = find_similar_keyword(reviews, keyword)
# for product, review, *rest in result:
#     reviewdict = {'product':product,'review':review,'date':rest[0],'marketplace':rest[1],'rating':rest[2],'sentiment':rest[3],'vine':rest[4]}
#     print(product, review, *rest, sep='\n')
#     print(reviewdict)






# import json
# from datetime import datetime
# import ast

# data = [["Fellowes","good","6 July 2022","United Kingdom","4.0","{'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.4404}","Verified Purchase"],["Fellowes","Good quality .. cleaned some button imprints off.","6 December 2021","United Kingdom","5.0","{'neg': 0.0, 'neu': 0.707, 'pos': 0.293, 'compound': 0.4404}","Verified Purchase"]]

# def avg_pos_reviews(data):
#     product_reviews = {}
#     for review in data:
#         product = review[0]
#         date_str = review[2]
#         sentiment = ast.literal_eval(review[5])
#         date = datetime.strptime(date_str, "%d %B %Y")
#         month_year = f"{date.month}/{date.year}"
        
#         if product not in product_reviews:
#             product_reviews[product] = {}
#         if month_year not in product_reviews[product]:
#             product_reviews[product][month_year] = {"total": 0, "positive": 0}
        
#         product_reviews[product][month_year]["total"] += 1
#         if sentiment["pos"] > sentiment["neg"]:
#             product_reviews[product][month_year]["positive"] += 1
    
#     avg_reviews = {}
#     for product, product_data in product_reviews.items():
#         avg_reviews[product] = {}
#         for month_year, review_data in product_data.items():
#             avg_reviews[product][month_year] = review_data["positive"] / review_data["total"]
    
#     return avg_reviews

# print(avg_pos_reviews(data))



# import json
# from datetime import datetime
# import ast

# data = [["Fellowes","good","6 July 2022","United Kingdom","4.0","{'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.4404}","Verified Purchase"],["Fellowes","Good quality .. cleaned some button imprints off.","6 December 2021","United Kingdom","5.0","{'neg': 0.0, 'neu': 0.707, 'pos': 0.293, 'compound': 0.4404}","Verified Purchase"]]

# def avg_pos_reviews(data):
#     product_reviews = {}
#     for review in data:
#         product = review[0]
#         date_str = review[2]
#         sentiment = ast.literal_eval(review[5])
#         date = datetime.strptime(date_str, "%d %B %Y")
#         month_year = f"{date.month}/{date.year}"
        
#         if product not in product_reviews:
#             product_reviews[product] = {}
#         if month_year not in product_reviews[product]:
#             product_reviews[product][month_year] = {"total": 0, "positive": 0}
        
#         product_reviews[product][month_year]["total"] += 1
#         if sentiment["pos"] > sentiment["neg"]:
#             product_reviews[product][month_year]["positive"] += 1
    
#     avg_reviews = []
#     for product, product_data in product_reviews.items():
#         for month_year, review_data in product_data.items():
#             avg_reviews.append({"product": product, "month_year": month_year, "product": review_data["positive"] / review_data["total"]})
    
#     return avg_reviews

# print(avg_pos_reviews(data))




# import json
# from datetime import datetime
# import ast

# data = [["Magicjell","good","6 July 2022","United Kingdom","4.0","{'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.4404}","Verified Purchase"],["Magicjell","good","6 july 2022","United Kingdom","4.0","{'neg': 1.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.4404}"],["Fellowes","Good quality .. cleaned some button imprints off.","6 December 2021","United Kingdom","5.0","{'neg': 0.0, 'neu': 0.707, 'pos': 0.293, 'compound': 0.4404}","Verified Purchase"]]

# def avg_pos_reviews(data):
#     product_reviews = {}
#     for review in data:
#         product = review[0]
#         date_str = review[2]
#         sentiment = ast.literal_eval(review[5])
#         date = datetime.strptime(date_str, "%d %B %Y")
#         month_year = f"{date.strftime('%B')} {date.year}"
        
#         if product not in product_reviews:
#             product_reviews[product] = {}
#         if month_year not in product_reviews[product]:
#             product_reviews[product][month_year] = {"total": 0, "positive": 0}
        
#         product_reviews[product][month_year]["total"] += 1
#         if sentiment["pos"] > sentiment["neg"]:
#             product_reviews[product][month_year]["positive"] += 1
    
#     avg_reviews = []
#     for product, product_data in product_reviews.items():
#         for month_year, review_data in product_data.items():
#             avg_reviews.append({product: review_data["positive"] / review_data["total"],"date": month_year})
    
#     avg_reviews = sorted(avg_reviews, key=lambda x: datetime.strptime(x['date'], "%B %Y"))
#     return avg_reviews

# print(avg_pos_reviews(data))



# from datetime import datetime, timedelta
# import json

# def average_rating(data, num_days=7, num_months=6, num_years=1):
#     now = datetime.now()
#     ratings = {}
#     for duration, num_units in zip(['7-day', '6-month', '1-year'], [num_days, num_months * 30, num_years * 365]):
#         ratings[duration] = sum(float(item[4]) for item in data if (now - datetime.strptime(item[2], '%d %B %Y')).days <= num_units) / len([item[4] for item in data if (now - datetime.strptime(item[2], '%d %B %Y')).days <= num_units]) if [item[4] for item in data if (now - datetime.strptime(item[2], '%d %B %Y')).days <= num_units] else None
#     return ratings

# data = [('Fellowes', 'good', '6 July 2022', 'United Kingdom', '4.0', "{'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.4404}", 'Verified Purchase'), ('MagicJell', 'Bought to clean finger grease from iPad touch screen. The wipes are almost dry when taken from the packet and whilst using two or three wipes does the job.', '24 April 2022', 'United Kingdom', '3.0', "{'neg': 0.0, 'neu': 0.956, 'pos': 0.044, 'compound': 0.4019}", 'Verified Purchase'), ('Fellowes', 'Came already dried out, and besides some idiot stuck a huge sticky label over the opening so you cannot reseal it after using.', '31 December 2022', 'United Kingdom', '1.0', "{'neg': 0.192, 'neu': 0.725, 'pos': 0.083, 'compound': -0.4588}", 'Verified Purchase'), ('Fellowes ', 'The size of the wipes are small the pack is handy for work or handbag as small packet. The wipes came practically dry with exception of the middle couple! Expensive screen clean!', '15 September 2022', 'United Kingdom', '1.0', "{'neg': 0.0, 'neu': 0.904, 'pos': 0.096, 'compound': 0.508}", 'Verified Purchase')]
# print(average_rating(data))

# from operator import itemgetter
# import ast

# reviews = [('Fellowes', 'good', '6 July 2022', 'United Kingdom', '1.0', "{'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.4404}", 'Verified Purchase'), ('MagicJell', 'Bought to clean finger grease from iPad touch screen. The wipes are almost dry when taken from the packet and whilst using two or three wipes does the job.', '24 April 2022', 'United Kingdom', '5.0', "{'neg': 0.0, 'neu': 0.956, 'pos': 0.044, 'compound': 0.4019}", 'Verified Purchase'), ('Fellowes', 'Came already dried out, and besides some idiot stuck a huge sticky label over the opening so you cannot reseal it after using.', '31 December 2022', 'United Kingdom', '1.0', "{'neg': 0.192, 'neu': 0.725, 'pos': 0.083, 'compound': -0.4588}", 'Verified Purchase'), ('Fellowes ', 'The size of the wipes are small the pack is handy for work or handbag as small packet. The wipes came practically dry with exception of the middle couple! Expensive screen clean!', '15 September 2022', 'United Kingdom', '1.0', "{'neg': 0.0, 'neu': 0.904, 'pos': 0.096, 'compound': 0.508}", 'Verified Purchase')]

# def recommend_product(reviews):
#     positive_reviews = [review for review in reviews if float(ast.literal_eval(review[5])["compound"]) > 0]
#     positive_reviews = sorted(positive_reviews, key=itemgetter(4), reverse=True)
#     if positive_reviews:
#         return positive_reviews[0][0]
#     else:
#         return None

# recommended_product = recommend_product(reviews)
# if recommended_product:
#     print(f"The recommended product is: {recommended_product}")
# else:
#     print("No product can be recommended as there are no positive reviews")


# from collections import defaultdict

# reviews = [    ('Fellowes', 'good', '6 July 2022', 'United Kingdom', '4.0', "{'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.4404}", 'Verified Purchase'),     ('MagicJell', 'Bought to clean finger grease from iPad touch screen. The wipes are almost dry when taken from the packet and whilst using two or three wipes does the job.', '24 April 2022', 'United Kingdom', '3.0', "{'neg': 0.0, 'neu': 0.956, 'pos': 0.044, 'compound': 0.4019}", 'Verified Purchase'),     ('Fellowes', 'Came already dried out, and besides some idiot stuck a huge sticky label over the opening so you cannot reseal it after using.', '31 December 2022', 'United Kingdom', '1.0', "{'neg': 0.192, 'neu': 0.725, 'pos': 0.083, 'compound': -0.4588}", 'Verified Purchase'),     ('Fellowes ', 'The size of the wipes are small the pack is handy for work or handbag as small packet. The wipes came practically dry with exception of the middle couple! Expensive screen clean!', '15 September 2022', 'United Kingdom', '1.0', "{'neg': 0.0, 'neu': 0.904, 'pos': 0.096, 'compound': 0.508}", 'Verified Purchase')]

# review_count = defaultdict(int)
# for product, review, date, country, rating, sentiment, verified_purchase in reviews:
#     date = date.split(" ")[-1]
#     review_count[(product, date)] += 1
    
# sorted_review_count = sorted(review_count.items(), key=lambda x: x[0][1])

# result = [{product: count, "date": date} for (product, date), count in sorted_review_count]

# print(result)






import mysql.connector

conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 
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

import spacy
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_sm")

# Define product description
product_description = 'Touchscreen Cleaning Wipes are ideal for cleaning tablets, smart phones and other multimedia devices. The wipes are perfect for removing finger prints and dirt from your touchscreen devices and include non-streak, anti-static properties. 12 packs are included in an outer and are attached to a clipstrip.'

# Define user inputs
user_features = ['wipes', 'screen', 'cleaning']
reviews = [('Magicjell', 'good', '6 July 2022', 'United Kingdom', '4.0', "{'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.4404}", 'Verified Purchase'),
           ('Fellowes', 'Bought to clean finger grease from iPad touch screen. The wipes are almost dry when taken from the packet and whilst using two or three wipes does the job.', '24 April 2022', 'United Kingdom', '3.0', "{'neg': 0.0, 'neu': 0.956, 'pos': 0.044, 'compound': 0.4019}", 'Vine'),
           ('Fellowes', 'Came already dried out, and besides some idiot stuck a huge sticky label over the opening so you cannot reseal it after using.', '31 December 2022', 'United Kingdom', '1.0', "{'neg': 0.192, 'neu': 0.725, 'pos': 0.083, 'compound': -0.4588}", 'Verified Purchase'),
           ('MagicJell', 'The size of the wipes are small the pack is handy for work or handbag as small packet. The wipes came practically dry with exception of the middle couple! Expensive screen clean!', '15 September 2022', 'United Kingdom', '1.0', "{'neg': 0.0, 'neu': 0.904, 'pos': 0.096, 'compound': 0.508}", 'Non-Verified Purchase')]

# Preprocess user features and product description
user_features = [nlp(feature) for feature in user_features]
product_doc = nlp(product_description)

# Extract features from product description
product_features = set([ent.text.lower() for ent in product_doc.ents] + [token.text.lower() for token in product_doc if token.pos_ == "NOUN"])

# Combine user features with product features
features = product_features.union(set([feature.text.lower() for feature in user_features]))

# Extract sentences from reviews that mention at least one feature
relevant_sentences = []
for review in reviews:
    review_doc = nlp(review[1])
    for sentence in review_doc.sents:
        if any([feature.text.lower() in sentence.text.lower() for feature in features]):
            relevant_sentences.append(sentence)

# Perform sentiment analysis on each relevant sentence
sentiment_scores = []
for sentence in relevant_sentences:
    sentiment_scores.append(nltk.sentiment.vader.SentimentIntensityAnalyzer().polarity_scores(sentence.text))

# Create TF-IDF vectorizer for sentence similarity analysis
tfidf_vectorizer = TfidfVectorizer(stop_words="english")

# Calculate TF-IDF scores for relevant sentences
sentence_texts = [sentence.text for sentence in relevant_sentences]
tfidf_scores = tfidf_vectorizer.fit_transform(sentence_texts)

# Identify most similar sentences
similarities = tfidf_scores * tfidf_scores.T
most_similar = []
for i,

# Extract the features from the reviews
feature_sentiments = defaultdict(list)
for review in reviews:
    doc = nlp(review[1])
    for sent in doc.sents:
        for feature in features:
            if feature in sent.text:
                sentiment = sia.polarity_scores(sent.text)['compound']
                feature_sentiments[feature].append(sentiment)

# Compute the average sentiment for each feature
feature_sentiment_averages = {}
for feature, sentiments in feature_sentiments.items():
    if len(sentiments) > 0:
        average_sentiment = sum(sentiments) / len(sentiments)
        feature_sentiment_averages[feature] = average_sentiment

# Sort the features by sentiment in descending order
sorted_features = sorted(feature_sentiment_averages.items(), key=lambda x: x[1], reverse=True)

# Generate extra features from the product description
doc = nlp(product_description)
for chunk in doc.noun_chunks:
    if chunk.root.text.lower() not in features:
        features.append(chunk.root.text.lower())

# Generate the output paragraph
positive_features = [feature[0] for feature in sorted_features if feature[1] > 0]
negative_features = [feature[0] for feature in sorted_features if feature[1] < 0]

output = f"Overall, the {product_name} is a great product that has several strong points. The {', '.join(positive_features)} are particularly impressive, and customers have praised them for their effectiveness and ease of use. However, there are also some areas where the {product_name} could be improved. In particular, customers have noted issues with the {', '.join(negative_features)}, and these are areas where the product could be made better. Despite these minor drawbacks, the {product_name} is a highly recommended product that is well worth considering for anyone in the market for {', '.join(features)}."

print(output)

# from collections import defaultdict
# import operator

# input_list = [("Magicjell", "good", "6 July 2022", "United Kingdom", "4.0", "{'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.4404}", "Verified Purchase"),
#               ("Fellowes", "Bought to clean finger grease from iPad touch screen. The wipes are almost dry when taken from the packet and whilst using two or three wipes does the job.", "24 April 2022", "United Kingdom", "3.0", "{'neg': 0.0, 'neu': 0.956, 'pos': 0.044, 'compound': 0.4019}", "Vine"),
#               ("Fellowes", "Came already dried out, and besides some idiot stuck a huge sticky label over the opening so you cannot reseal it after using.", "31 December 2022", "United Kingdom", "1.0", "{'neg': 0.192, 'neu': 0.725, 'pos': 0.083, 'compound': -0.4588}", "Verified Purchase"),
#               ("MagicJell", "The size of the wipes are small the pack is handy for work or handbag as small packet. The wipes came practically dry with exception of the middle couple! Expensive screen clean!", "15 September 2022", "United Kingdom", "1.0", "{'neg': 0.0, 'neu': 0.904, 'pos': 0.096, 'compound': 0.508}", "Non-Verified Purchase")]

# product_dict = defaultdict(lambda: {'total_reviews': 0, 'positive_comments': 0, 'negative_comments': 0, 'average_rating': 0, 'vine_reviews': 0, 'verified_purchases': 0, 'non_verified_purchases': 0})

# for product_name, review, date, marketplace, rating, sentiment, product_type in input_list:
#     rating = float(rating)
#     sentiment_dict = eval(sentiment)
#     sentiment_score = sentiment_dict['pos'] - sentiment_dict['neg']
#     if sentiment_score > 0:
#         product_dict[product_name]['positive_comments'] += 1
#     elif sentiment_score < 0:
#         product_dict[product_name]['negative_comments'] += 1
#     product_dict[product_name]['total_reviews'] += 1
#     product_dict[product_name]['average_rating'] += rating
#     if product_type == 'Vine':
#         product_dict[product_name]['vine_reviews'] += 1
#     elif product_type == 'Verified Purchase':
#         product_dict[product_name]['verified_purchases'] += 1
#     elif product_type == 'Non-Verified Purchase':
#         product_dict[product_name]['non_verified_purchases'] += 1

# # calculate average rating
# for product_name in product_dict:
#     if product_dict[product_name]['total_reviews'] > 0:
#         product_dict[product_name]['average_rating'] /= product_dict[product_name]['total_reviews']

# # sort the product_dict by positive_comments and average_rating
# sorted_products = sorted(product_dict.items(), key=lambda x: (-x[1]['positive_comments'], -x[1]['average_rating']))


# def get_ranking(item):
#     average_rating = item[1]['average_rating']
#     positive_comments = item[1]['positive_comments']
#     negative_comments = item[1]['negative_comments']
#     sentiment_bias = (positive_comments - negative_comments) / (positive_comments + negative_comments)
#     return average_rating * sentiment_bias

# data_with_ranking = sorted(sorted_products, key=get_ranking, reverse=True)

# for i, item in enumerate(data_with_ranking):
#     item[1]['ranking'] = i + 1

# print(data_with_ranking)


conn.close()
c.close()



# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer

# # Create SentimentIntensityAnalyzer object to calculate sentiment scores
# sia = SentimentIntensityAnalyzer()

# # Define list of features for the product
# product_features = ['screen', 'wipes', 'size', 'packaging', 'price']

# # Define list of reviews
# reviews = [("Magicjell", "good"), 
#            ("Fellowes", "Bought to clean finger grease from iPad touch screen. The wipes are almost dry when taken from the packet and whilst using two or three wipes does the job."),
#            ("Fellowes", "Came already dried out, and besides some idiot stuck a huge sticky label over the opening so you cannot reseal it after using."),
#            ("MagicJell", "The size of the wipes are small the pack is handy for work or handbag as small packet. The wipes came practically dry with exception of the middle couple! Expensive screen clean!")]

# # Define dictionary to store sentiment scores for each feature
# feature_sentiments = {}

# # Loop over each feature and calculate its sentiment score based on the reviews
# for feature in product_features:
#     sentiment_scores = []
#     for review in reviews:
#         # Check if the feature is mentioned in the review
#         if feature in review[1]:
#             # Calculate the sentiment score for the review
#             sentiment_score = sia.polarity_scores(review[1])['compound']
#             sentiment_scores.append(sentiment_score)
#     # Calculate the average sentiment score for the feature
#     if sentiment_scores:
#         feature_sentiments[feature] = sum(sentiment_scores) / len(sentiment_scores)

# # Sort the features by their sentiment score in descending order
# sorted_features = sorted(feature_sentiments.items(), key=lambda x: x[1], reverse=True)

# # Print the top 3 features and suggestions for improvement
# print("Top 3 features to improve:")
# for feature, sentiment_score in sorted_features[:3]:
#     print(f"{feature.capitalize()}:")
#     if sentiment_score > 0:
#         print("- Customers like this feature, consider enhancing it further.")
#     else:
#         print("- Customers are not satisfied with this feature, consider improving it.")
#     print()
