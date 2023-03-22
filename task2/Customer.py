from Review import Review
from Beverage import Beverage
from Cafe import Cafe

class Customer:
    
    def __init__(self, name: str, balance: float, discount: float = None) -> None:
        if balance < 0:
            raise ValueError(f'Balance cannot be negative: {balance}')
        try:
            self.name = str(name)
            self.balance = float(round(balance, 2))
            self.discount = float(round(discount, 2)) if discount else None
            self.order = []
            self.total = 0
        except ValueError:
            print('Value is in incorrect format')

    def __repr__(self) -> str:
        return f'name: {self.name}, balance: {self.balance} discount: {self.discount}'

    @staticmethod    
    def from_json(customer_data) -> object:
        return Customer(customer_data['name'], customer_data['balance'], customer_data['discount'])

    def to_json(self) -> object:
            order = list(map(lambda x: x.to_json(), self.order))
            return {
                'name': self.name,
                'balance': round(self.balance, 2),
                'discount': self.discount,
                'order': order,
                'total': round(self.total, 2),
            }

    @staticmethod
    def get_customer_with_highest_balance(customers: list) -> object:
        if not customers:
            return None
        return max(customers, key=lambda customer: customer.balance)

    def add_order_item(self, cafe: Cafe, beverage: Beverage) -> object:
        assert beverage in cafe.menu, f'{cafe.name} does not serve {beverage.name}'
        self.order.append(beverage)
        self.total += beverage.price
        return self

    def remove_order_item(self, beverage: Beverage) -> object:
        assert beverage in self.order, 'Beverage to be removed not in order'
        self.order.remove(beverage)
        self.total -= beverage.price
        return self

    def place_order(self, cafe: Cafe) -> object:
        if self.discount:
            self.total *= (1 - self.discount)
        cafe.place_order(self, self.total, self.balance)
        return self
    
    def submit_review(self, cafe: Cafe, review: Review) -> object:
        for r in cafe.reviews:
            if r.author == review.author and r.description == review.description:
                raise ValueError(f'Review already exists: {review.__repr__()}')
        cafe.reviews.append(review)
        print(f'Review submitted successfully to {cafe.name}')
        return self
