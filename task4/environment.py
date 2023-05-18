from datetime import datetime
import queue
import requests
import sys
import threading
import time
from bs4 import BeautifulSoup
from cafe.beverage import Beverage
from cafe.cafe import Cafe
from cafe.customer import Customer
from cafe.ingredient import Ingredient
from cafe.recipe import Recipe
from cafe.review import Review
import json_reader


def scrape_cafe(cafe, menu, results = None):

    name = cafe.text
    url = f"https://www.yelp.com{cafe['href']}"
    response = requests.get(url)

    if not response.ok:
        sys.exit('Server refused HTTP request')

    cafe_data = BeautifulSoup(response.text, 'html.parser')

    address = cafe_data.find('address').text

    if not address:
        address = 'Address unavailable'

    reviews = cafe_data.find_all('div', 'review__09f24__oHr9V')
    cafe = Cafe(name, address, menu, [])

    for review in reviews[:4]:
        name = review.find('div', class_='user-passport-info border-color--default__09f24__NPAKY').text.split('.')[0] + '.'
        rating = float(review.find('div', class_='five-stars__09f24__mBKym')['aria-label'][0])
        description = review.find('p', 'comment__09f24__gu0rG css-qgunke').text
        date = datetime.strptime(review.find('span', 'css-chan6m').text, '%m/%d/%Y').strftime('%Y-%m-%d')

        cafe.reviews.append(Review(name, rating, description, date))

    if results:
        results.put(cafe)
    else:
        return cafe

def demo(cafes):

    print('DEMO START')

    customer_dave, customer_claire, customer_nikita = customers

    #customer methods
    print('\nDave:')
    customer_dave.add_order_item(cafes[0], cafes[0].menu[0]) \
                .add_order_item(cafes[0], cafes[0].menu[1]) \
                .place_order(cafes[0]) \
                .submit_review(cafes[0], Review(customer_dave.name, 5.0, 'Good coffee and customer service', '2023-02-02'))


    print('\nNikita:')
    customer_nikita.submit_review(cafes[0], Review(customer_nikita.name, 3.5, 'Decent coffee but rude waiters', '2023-01-23')) \
        .submit_review(cafes[0], Review(customer_nikita.name, 4.5, 'Better waiters this time', '2023-01-24')) \
        .add_order_item(cafes[1], cafes[1].menu[0]) \
        .add_order_item(cafes[1], cafes[1].menu[1])


    print('\nClaire:')
    customer_claire.add_order_item(cafes[1], cafes[1].menu[0]) \
        .place_order(cafes[1])    

    new_customer = Customer('John', 1.9, 0.1)
    new_customer.add_order_item(cafes[1], cafes[1].menu[1]) \
        .place_order(cafes[1])
    customers.append(new_customer)

    #static method
    print(f'\nCustomer with highest balance: {Customer.get_customer_with_highest_balance(customers)}')

    #cafe methods
    print(f'\n{cafes[0].name}:')
    cafes[0].add_menu_item(beverages[-1]) \
        .remove_menu_item(beverages[-2])
    print(f'{cafes[0].name} average rating: {cafes[0].calculate_average_rating()}')
    print(f'Average amount of days between reviews: {cafes[0].calculate_average_time_between_reviews()} days')

    print('\nPrice per unit for all beverages:')
    for beverage in beverages:
        print(f'{beverage.name}: {beverage.calculate_ppu()}')

    new_cafe = Cafe('New Cafe', 'Address 123')
    new_cafe.add_menu_item(beverages[1])
    new_cafe.add_menu_item(beverages[2])
    cafes.append(new_cafe)

    # write objects to file
    json_reader.write_json_to_file('./json/ingredient_altered.json', ingredients)
    json_reader.write_json_to_file('./json/recipe_altered.json', recipes)
    json_reader.write_json_to_file('./json/beverage_altered.json', beverages)
    json_reader.write_json_to_file('./json/cafe_altered.json', cafes)
    json_reader.write_json_to_file('./json/customer_altered.json', customers)

    print('\nDEMO END')

if __name__ == '__main__':
    
    # Clear any data from previous scrape
    open('./json/scraped.json', 'w')

    # Load objects from json
    ingredients = json_reader.load_data('./json/ingredient.json', Ingredient)
    recipes = json_reader.load_data('./json/recipe.json', Recipe)
    beverages = json_reader.load_data('./json/beverage.json', Beverage)
    customers = json_reader.load_data('./json/customer.json', Customer)

    mock_menu = beverages

    url = 'https://www.yelp.com/search?find_desc=cafe&find_loc=New_York'

    # Send GET request to the URL
    response = requests.get(url)
    if not response.ok:
        sys.exit('Server refused HTTP request')
    else:
        print(f'HTTP request response: {response} (ok)\n')

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the cafes on the page
    cafes = soup.find_all('a', class_='css-19v1rkv')

    results = queue.Queue()
    threads = []
    cafe_obj = []

    # Threading comparison start
    start_time = time.time()

    # first 4 objects arent reviews, so 14-4 = 10 cafe objects
    # 1 cafe object with 4 review objects * 10 = 50 objects total
    for cafe in cafes[3:14]:
        thread = threading.Thread(target=scrape_cafe, args=(cafe, mock_menu, results))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    while not results.empty():
        cafe = results.get()
        cafe_obj.append(cafe)

    end_time = time.time()
    print(f'Threading total time: {end_time - start_time} sec.\n')
    # Threading comparison end

    # Non-threading comparison start
    # start_time = time.time()

    # cafe_obj = []
    # for cafe in cafes[3:14]:
    #     cafe_obj.append(scrape_cafe(cafe, mock_menu))

    # end_time = time.time()
    # print(f'Non-hreading total time: {end_time - start_time} sec.\n')
    # Non-threading comparison end

    json_reader.write_json_to_file('./json/scraped.json', cafe_obj, 'a+')
    cafes = json_reader.load_data('./json/scraped.json', Cafe)

    demo(cafes)

__all__ = ['demo', 'scrape_cafe']