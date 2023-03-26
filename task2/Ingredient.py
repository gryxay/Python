class Ingredient:
    
    def __init__(self, name: str, calories: int, price: float) -> None:
        try:
            self.name = str(name)
            self.calories = int(calories)
            self.price = float(round(price, 2))
        except ValueError:
            print('Value is in incorrect format')

    def __repr__(self) -> str:
        return f'name: {self.name}, calories: {self.calories}, price: {self.price}'
    
    @staticmethod
    def from_json(data: dict) -> object:
        return Ingredient(data['name'], data['calories'], data['price'])

    def to_json(self) -> object:
        return {
            'name': self.name,
            'calories': self.calories,
            'price': round(self.price, 2),
        }