class Transfer:
    def __init__(self, fromClub, toClub, player, player_age, fee, season, period, isLoan, league):
        self.fromClub = fromClub
        self.toClub = toClub
        self.player = player
        self.fee : float = fee
        self.season = season
        self.period = period
        self.isLoan = isLoan
        self.league = league
        self.player_age = player_age
        self.international = fromClub.country != toClub.country
        self.group_name = None

    def __eq__(self, other):
        return self.season == other.season and      \
               self.fromClub == other.fromClub and  \
               self.toClub == other.toClub and      \
               self.fee == other.fee and            \
               self.isLoan == other.isLoan 

    def __lt__(self, other):
        if self.season != other.season:
            return self.season < other.season
        if self.fromClub != other.fromClub:
            return self.fromClub < other.fromClub
        if self.toClub != other.toClub:
            return self.toClub < other.toClub
        if self.player != other.player:
            return self.player < other.player
        if self.period != other.period:
            return self.period < other.period
        return False

    def __str__(self):
        return self.player.__str__() + ": " + \
               self.fromClub.__str__() + " -> " + self.toClub.__str__() + \
               (", loaned for " if self.isLoan else ", sold for ") + \
               str(self.fee) + "M, during " + self.season.__str__()

    def __hash__(self):
        return self.fromClub.name.__hash__() + \
            1000000007*self.toClub.name.__hash__() + \
            5915587277*self.player.name.__hash__()

    def toArray(self):
        arr = []
        arr.append(self.fromClub.name)
        arr.append(self.toClub.name)
        arr.append(self.league)
        arr.append(self.player.name)
        arr.append(self.player_age)
        arr.append(self.player.position)
        arr.append(str(self.fee)+"M" if self.fee != 0 else "NA")
        arr.append(("on loan" if self.isLoan else "sold"))
        arr.append(self.period)
        arr.append(self.season.year)
        arr.append(self.season.season)
        arr.append("international" if self.international else "local")
        arr.append(self.fromClub.country)
        arr.append(self.toClub.country)
        if self.group_name:
            arr.append(self.group_name)
        return arr
