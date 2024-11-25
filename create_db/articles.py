import csv
from funzioni_db import *

def insert_articles():
    with open('EtsyListingsDownload.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)

        articles = []
        id = 0

        #INSERT ARTICLES
        for row in reader:
            id += 1
            item = {}

            item['id'] = id
            item['item'] = row[0]
            item['description'] = row[1]
            item['price'] = round(float(row[2]),2)
            item['quantity'] = row[4]
            item['category_id'] = 1

            articles.append(item)
            #print(item)
            print(row)

        #INSERT IMAGES

    print(articles)

insert_articles()