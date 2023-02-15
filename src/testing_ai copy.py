import nltk
import spacy

nltk.download('punkt')

nlp = spacy.load('en_core_web_sm')

def find_sentences_with_keyword(reviews, keyword):
    keyword = keyword.lower()
    sentences_with_keyword = []
    for review in reviews:
        review_text = review[1]
        sentences = nltk.sent_tokenize(review_text)
        for sentence in sentences:
            doc = nlp(sentence)
            if any(token.text.lower() == keyword or token.lemma_.lower() == keyword for token in doc):
                sentences_with_keyword.append(sentence)
    return sentences_with_keyword

reviews = [
    ('Magicjell', 'good', '6 July 2022', 'United Kingdom', '4.0', "{'neg': 0.0, 'neu': 0.0, 'pos': 1.0, 'compound': 0.4404}", 'Verified Purchase'),
    ('Fellowes', 'Bought to clean finger grease from iPad touch screen. The wipes are almost dry when taken from the packet and whilst using two or three wipes does the job.', '24 April 2022', 'United Kingdom', '3.0', "{'neg': 0.0, 'neu': 0.956, 'pos': 0.044, 'compound': 0.4019}", 'Vine'),
    ('Fellowes', 'Came already dried out, and besides some idiot stuck a huge sticky label over the opening so you cannot reseal it after using.', '31 December 2022', 'United Kingdom', '1.0', "{'neg': 0.192, 'neu': 0.725, 'pos': 0.083, 'compound': -0.4588}", 'Verified Purchase'),
    ('MagicJell', 'The size of the wipes are small the pack is handy for work or handbag as small packet. The wipes came practically dry with exception of the middle couple! Expensive screen clean!', '15 September 2022', 'United Kingdom', '1.0', "{'neg': 0.0, 'neu': 0.904, 'pos': 0.096, 'compound': 0.508}", 'Non-Verified Purchase')
]

keyword = "wipes"

print(find_sentences_with_keyword(reviews, keyword))