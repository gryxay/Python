import json
import os
from Cafe import Cafe
from Recipe import Recipe
from Beverage import Beverage
from Customer import Customer
from Ingredient import Ingredient
from Review import Review

def load_data(file_path, obj_class):
    assert(os.path.getsize(file_path) > 0), f'Empty file encountered: {file_path}'
    with open(file_path, 'r') as f:
        data = json.load(f)
        objects = [obj_class.from_json(obj_data) for obj_data in data]
        return objects

def write_json_to_file(file_path, object_list):
    with open(file_path, 'w') as f:
        json_strings = [json.dumps(obj.to_json(), indent=4) for obj in object_list]
        f.write(f'[\n' + ',\n'.join(json_strings) + '\n]')


# load objects from json
ingredients = load_data('./json/ingredient.json', Ingredient)
recipes = load_data('./json/recipe.json', Recipe)
beverages = load_data('./json/beverage.json', Beverage)
cafes = load_data('./json/cafe.json', Cafe)
customers = load_data('./json/customer.json', Customer)

# demo setup
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
print('\nCafeInn:')
cafes[0].add_menu_item(beverages[-1]) \
    .remove_menu_item(beverages[-2])
print(f'CafeInn average rating: {cafes[0].calculate_average_rating()}')
print(f'Average amount of days between reviews: {cafes[0].calculate_average_time_between_reviews()} days')
print(f'Cafe latitude and longitude: {cafes[0].get_location_from_address()}')

print('\nPrice per unit for all beverages:')
for beverage in beverages:
    print(f'{beverage.name}: {beverage.calculatePPU()}')

new_cafe = Cafe('New Cafe', 'Address 123')
new_cafe.add_menu_item(beverages[1])
new_cafe.add_menu_item(beverages[2])
cafes.append(new_cafe)

# write objects to file
write_json_to_file('./json/ingredient_altered.json', ingredients)
write_json_to_file('./json/recipe_altered.json', recipes)
write_json_to_file('./json/beverage_altered.json', beverages)
write_json_to_file('./json/cafe_altered.json', cafes)
write_json_to_file('./json/customer_altered.json', customers)