import json
import sqlite3

connection = sqlite3.connect('./database/database.db')

with open('./database/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open('./json/scraped.json') as json_file:
    cafes_data = json.load(json_file)

for index, cafe in enumerate(cafes_data):
    name = cafe['name']
    location = cafe['location']
    menu = cafe['menu']
    reviews = cafe['reviews']
    
    cur.execute("INSERT INTO cafes (name, location) VALUES (?, ?)",
            (name, location))
    
    for menu_item in menu:
        cafe_id = index
        name = menu_item['name']
        recipe = menu_item['recipe']['instructions']
        price = menu_item['price']

        cur.execute("INSERT INTO beverages (cafeId, name, recipe, price) VALUES (?, ?, ?, ?)",
            (cafe_id, name, recipe, price))

    for review in reviews:
        cafe_id = index
        author = review['author']
        rating = review['rating']
        description = review['description']
        date = review['date']

        cur.execute("INSERT INTO reviews (cafeId, author, rating, description, date) VALUES (?, ?, ?, ?, ?)",
            (cafe_id, author, rating, description, date))

connection.commit()
connection.close()
