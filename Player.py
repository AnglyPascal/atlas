import Transferable

class Player(Transferable.Transferable):
    def __init__(self, name: str, birth_year: int, position: str):
        super().__init__()
        self.name = name
        self.birth_year = birth_year
        self.position = position

    def __str__(self):
        return self.name + ", " + self.position

    def __lt__(self, other):
        if self.name < other.name:
            return True
        if self.position < other.position:
            return True
        if self.birth_year < other.birth_year:
            return True
        return False
