class Review:
    
    def __init__(self, author: str, rating: float, description: str, date: str) -> None:
        try:
            self.author = str(author)
            self.rating = float(round(rating, 1))
            self.description = str(description)
            self.date = str(date)
        except ValueError:
            print('Value is in incorrect format')

    def __repr__(self) -> str:
        return f'author: {self.author}, rating: {self.rating}, description: {self.description}, date: {self.date}'
    
    @staticmethod
    def from_json(data: str) -> object:
        return Review(data['author'], data['rating'], data['description'], data['date'])

    def to_json(self) -> object:
        return {
            'author': self.author,
            'rating': self.rating,
            'description': self.description,
            'date': self.date,
        }