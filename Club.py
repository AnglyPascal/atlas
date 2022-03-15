import Transferable

class Club(Transferable.Transferable):
    def __init__(self, name, country):
        super().__init__()
        self.name = name
        self.country = country

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name
