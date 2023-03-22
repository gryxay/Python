from datetime import datetime
import pip._vendor.requests as requests
from Beverage import Beverage
from Review import Review

class Cafe:

    def __init__(self, name: str, location: str, menu: list = None, reviews: list = None) -> None:
        try:
            self.name = str(name)
            self.location = str(location)
            self.menu = [] if menu is None else menu
            self.reviews = [] if reviews is None else reviews
        except ValueError:
            print('Value is in incorrect format')

    def __repr__(self) -> str:
        return f'name: {self.name}, address: {self.location}\nmenu: {list(map(lambda x: x.__repr__(), self.menu))}\nreviews: {self.reviews}\n'

    @staticmethod
    def from_json(data: str) -> object:
        beverages = []
        reviews = []
        for beverage in data['menu']:
            beverages.append(Beverage.from_json(beverage))
        for review in data['reviews']:
            reviews.append(Review.from_json(review))
        return Cafe(data['name'], data['location'], beverages, reviews)

    def to_json(self) -> object:
        beverages = []
        if self.menu:
            beverages = list(map(lambda x: x.to_json(), self.menu))
        reviews = []
        if self.reviews:
            reviews = list(map(lambda x: x.to_json(), self.reviews))
        return {
            'name': self.name,
            'location': self.location,
            'menu': beverages,
            'reviews': reviews,
        }

    def get_location_from_address(self) -> tuple:
        # OpenStreetMap API for retrieving the latitude and longitude of an address
        url = f'https://nominatim.openstreetmap.org/search/{self.location}?format=json&addressdetails=1&limit=1'
        response = requests.get(url).json()

        if response:
            location = response[0]
            return float(location['lat']), float(location['lon'])
        else:
            raise ValueError(f'Unable to retrieve location for address: {self.location}')

    def add_menu_item(self, beverage: Beverage) -> object:
        self.menu.append(beverage)
        return self

    def remove_menu_item(self, beverage: Beverage) -> object:
        for b in self.menu:
            if b.name == beverage.name:
                self.menu.remove(b)
                return self
        raise ValueError(f'Menu item to be removed not in menu: {beverage.name}')

    def place_order(self, customer, total: float, balance: float) -> bool:
        float(balance)
        assert total <= balance, 'Balance insufficient: {customer.balance}'
        print('Order successful!')
        customer.balance -= total
        customer.order = []
        return True
        
    def calculate_average_rating(self) -> float:
        if len(self.reviews) == 0:
            return None
        if len(self.reviews) < 2:
            return round(float(self.reviews[0]), 2)
        sum = 0.0
        for review in self.reviews:
            sum += float(review.rating)
        return round(float(sum/len(self.reviews)), 2)
    
    def calculate_average_time_between_reviews(self) -> int:
        if len(self.reviews) < 2:
            return None
        deltas = []
        for i in range(1, len(self.reviews)):
            delta = datetime.strptime(self.reviews[i-1].date, '%Y-%m-%d') - datetime.strptime(self.reviews[i].date, '%Y-%m-%d')
            deltas.append(delta.days)
        average_time = abs(sum(deltas)/(len(self.reviews)-1))
        return round(int(average_time),2)
