import Transferable

class Club(Transferable.Transferable):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name
