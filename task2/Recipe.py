from Ingredient import Ingredient

class Recipe:
    
    def __init__(self, name: str, ingredients: list, instructions: str) -> None:
        try:
            self.name = str(name)
            self.ingredients = list(ingredients)
            self.instructions = str(instructions)
        except ValueError:
            print('Value is in incorrect format')

    def __repr__(self) -> str:
        return f'name: {self.name}, ingredients: {self.ingredients}, instructions: {self.instructions}'

    @staticmethod
    def from_json(data: str) -> object:
        ingredients = []
        for ingredient in data['ingredients']:
            ingredients.append(Ingredient.from_json(ingredient))
        return Recipe(data['name'], ingredients, data['instructions'])

    def to_json(self) -> object:
        ingredients = list(map(lambda x: x.to_json(), self.ingredients))
        return {
            'name': self.name,
            'ingredients': ingredients,
            'instructions': self.instructions,
        }