from .recipe import Recipe

class Beverage:
    
    def __init__(self, name: str, recipe: Recipe, price: float) -> None:
        try:
            self.name = str(name)
            self.recipe = recipe
            self.price = float(round(price, 2))
        except ValueError:
            print('Value is in incorrect format')
    
    def __repr__(self) -> str:
        return f'name: {self.name}, recipe: {self.recipe}, price: {self.price}'

    @staticmethod
    def from_json(data: dict) -> object:
        recipe = Recipe.from_json(data['recipe'])
        return Beverage(data['name'], recipe, data['price'])


    def to_json(self) -> object:
        return {
            'name': self.name,
            'recipe': self.recipe.to_json(),
            'price': round(self.price, 2),
        }

    def calculate_ppu(self) -> float:
        # calculates production price per unit
        price = sum(ingredient.price for ingredient in self.recipe.ingredients)
        return float(round(price, 2))
    
    def calculate_calories(self) -> int:
        calories = 0
        for ingredient in self.recipe.ingredients:
            calories += ingredient.calories
        
        return int(calories)
    
__all__ = ['Beverage']
