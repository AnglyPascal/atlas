import Transferable

class Season(Transferable.Transferable):
    def __init__(self, year, season):
        super().__init__()
        self.year = year
        self.season = season

    def __str__(self):
        return self.season

    def __lt__(self, other):
        return self.season < other.season
