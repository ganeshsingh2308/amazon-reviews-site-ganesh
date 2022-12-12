
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
rowheader = ['Text']
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment = SentimentIntensityAnalyzer()

import mysql.connector
import re

conn = mysql.connector.connect(host="localhost",user='root',password='root123',database='main') 

c = conn.cursor()


# web = 'https://www.amazon.co.uk/Reusable-Cold-Compress-Premium-Ankle/dp/B07XQK77LR/ref=sr_1_1_sspa?crid=BW8V30GS8D9A&keywords=magic+gel&qid=1668781338&sprefix=magicjell%2Caps%2C93&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1'
driver_path = './drivers/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--headless')

next_page = ''
product_review = []
allreviews = []
alldates = []
allratings = []
allnames = []

def scrape_amazon(web):
    c = conn.cursor()
    page_number = 1

    driver = webdriver.Chrome(service = Service(executable_path=driver_path))
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
    driver.get(web)
    driver.implicitly_wait(5)
    review_page = str(driver.find_element(By.XPATH, '//a[@class ="a-link-emphasis a-text-bold"]').get_attribute("href"))
    driver.get(review_page)
    driver.implicitly_wait(5)
    page = driver.find_element(By.XPATH, '//div[@class ="a-row a-spacing-base a-size-base"]')
    page1 = str(page.text)
    test1 = page1.replace(',','')
    pages = [int(s) for s in re.findall(r'\b\d+\b', test1)]
    
    
    while page_number <= ((pages[1]/10)-1):
        scrape_page(driver)
        driver.get(next_page)
        driver.implicitly_wait(5)
        page_number += 1
    driver.quit()
    print(product_review)
    with open ('./project/data1.csv','w') as csvfile:
        write = csv.writer(csvfile)
        write.writerow(rowheader)
        for review in product_review:
            write.writerow([review])
    for i in range(0,len(allreviews)):
        sent_1 = str(sentiment.polarity_scores(allreviews[i]))
        c = conn.cursor()
        c.execute("INSERT INTO reviews1 (product,review,date,rating,sentiment) VALUES (%s,%s,%s,%s,%s)",(allnames[0], allreviews[i], alldates[i], allratings[i],sent_1))
        conn.commit()
    
    allnames2 = []
    allnames2.append(allnames[0])
    c = conn.cursor()
        
    c.execute("INSERT INTO productnames (product) VALUE (%s)",(allnames2))
    conn.commit()
    linkstring = []
    linkstring.append(str(web))
    c.execute("INSERT INTO amazonlink (link,product) VALUES (%s,%s)",(str(web),allnames[0]))
    conn.commit()
    conn.close()
    c.close()
    return 'test'


    
    

def scrape_page(driver):

    items = wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "a-section review aok-relative")]')))
    for item in items:
        product_details = {}
        # find name
        review = item.find_element(By.XPATH, './/span[@class= "a-size-base review-text review-text-content"]')
        date = item.find_element(By.XPATH, './/span[@class= "a-size-base a-color-secondary review-date"]')
        rating = str(item.find_element(By.XPATH, './/a[@class= "a-link-normal"]').get_attribute("title"))
        product_details = {'Review' : review.text, 'date' : date.text, 'rating' : rating}
        product_review.append(product_details)
        allreviews.append(review.text)
        alldates.append(date.text)
        allratings.append(rating)

    items2 = driver.find_element(By.XPATH, '//div[contains(@class, "a-fixed-left-grid-col product-info a-col-right")]')
    name = items2.find_element(By.XPATH, './/a[@class= "a-link-normal"]')
    name2 = str(name.text).replace("'","")
    allnames.append(name2)
    

    global next_page
    next_page = str(driver.find_element(By.XPATH, '//li[@class ="a-last"]/a').get_attribute("href"))



# scrape_amazon(18,'https://www.amazon.co.uk/Reusable-Cold-Compress-Premium-Ankle/dp/B07XQK77LR/ref=sr_1_1_sspa?crid=BW8V30GS8D9A&keywords=magic+gel&qid=1668781338&sprefix=magicjell%2Caps%2C93&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1')

