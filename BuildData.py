import os
import csv
import json
from typing import Dict
from Transfer import Transfer
from Club import Club
from Player import Player
from Season import Season

class BuildData:
    """ Class to do all the heavy lifting

        It first reads all the csv file present in the ./data directory
        Then it combines them into a single array that has all the transactions in forms of arrays

        Then we go over the array and create the Club, Player and Season objects, deatils of which
        are explained in the appropriate places. 

        We then go over the array once more, and create Transfer objects, and add them to related 
        Club, Player and Season objects.
    """
    def __init__(self, dirName: str = None):
        # the key is the fullname of the clubs
        self.clubs: Dict[str, Club]     = {}
        # clubNames hold maps from club abbreviation/nicknames to fullnames
        # so that we can avoid repetitions in Club objects
        self.clubNames: Dict[str, str]  = {}
        # the key is the name of the player
        self.players: Dict[str, Player] = {}
        # the key is the season string of the format 2020/2021
        self.seasons: Dict[str, Season] = {}
        # transfersArray holds all the transfers, useful for queries
        self.transfersArray = set()
        # if the data is stored in somewhere other than ./data, 
        # it can be passed to the constructor
        self.dirName = dirName

        # fixing some corner cases with club name abbreviations and nicknames
        with open("outcasts.json", "r") as outcastFile:
            self.outcastClubNames = json.load(outcastFile)

        # here we initiate our data structure
        self.createObjects()



    def getClub(self, name) -> Club:
        """ Given club name, return the Club object associated to that name, 
            ignores abbreviations 
        """
        name = self.truncate(name)
        return self.clubs[self.clubNames[name]]

    def getPlayer(self, name) -> Player:
        """ Given player name, return the Player object associated to this name """
        return self.players[name]

    def getSeason(self, season) -> Season:
        """ Given season string of the format 2020/2021, 
            return the Season object associated to this season
        """
        return self.seasons[season]

    def addTransfer(self, array: list[str]):
        """ Given a array representing a transfer, create a Transfer object,
            and add it to respective Club, Player, Season objects
        """
        # the transfer represents a retirement of a player
        if array[4] == "Retired":
            return
        # the club from which the player was transferred
        fromClub: Club = self.getClub(array[4]) if array[6] == "in" else self.getClub(array[0])
        # the club to which the player was transferred
        toClub: Club   = self.getClub(array[0]) if array[6] == "in" else self.getClub(array[4])
        # if the tranfers was within the club, discard it
        if fromClub == toClub:
            return
        # the player that was transferred
        player: Player = self.getPlayer(array[1])
        # the season in which the transfer happened
        season: Season = self.getSeason(array[11])
        # the amount of transaction involved in the transfer
        try:
            fee: float = float(array[8])
        # it might be NA or -
        except ValueError: 
            fee: float = 0
        # check in the 5th field for the word loan, 
        # indicating that this transfer was a loan
        isLoan: bool = "loan" in array[5] or "Loan" in array[5]
        # period of the transfer
        period: str = array[7]
        # the league in which this transfer happened
        league: str = array[9]
        # age of the player during this transfer
        age: str = array[2]

        ## create the Transfer object
        transfer = Transfer(fromClub, toClub, player, age, fee, season, period, isLoan, league)
        ## add it to all the other related objects
        fromClub.addTransfer(transfer)
        toClub.addTransfer(transfer)
        player.addTransfer(transfer)
        season.addTransfer(transfer)
        self.transfersArray.add(transfer)


    def truncate(self, name):
        nameArr = name.split(" ")
        secondary = ["II", "2", "B", "C", "U17", "U18", "Y19", "U19", "U20", "U21", "U22", "U23"]
        for s in secondary:
            if s == nameArr[-1]:
                nameArr = nameArr[:-1]
        return " ".join(nameArr) 

    def createObjects(self):
        """ Process the data from the files and create all the necessary 
            objects representing the data structure.
        """
        transfersArray = self.combineTransfers()

        # This loop gets all the full names of the clubs from the first column and creates
        # Club objects with those. The last element of the array represents the country of
        # this club assuming that's how the data was stored. 
        # 
        # It also creates Season objects and Player objects
        for array in transfersArray:
            club_name: str = array[0]
            if club_name not in self.clubNames:
                self.clubNames[club_name] = club_name
                self.clubs[club_name] = Club(club_name, array[-1])

            season_name: str = array[11]
            if season_name not in self.seasons:
                self.seasons[season_name] = Season(array[10], array[11])

            player_name: str = array[1]
            if player_name not in self.players:
                try:
                    birth_year: int = int(array[10]) - int(array[2])
                except ValueError:
                    birth_year: int = -1
                position: str = array[3]
                self.players[player_name] = Player(player_name, birth_year, position)

        # This for loop checks all the club names on the fourth column and checks if any
        # of those names is actually an abbreviation of already present club names. If
        # not, we create a new Club object for those clubs
        for array in transfersArray:
            club_name: str = self.truncate(array[4])
            if club_name not in self.clubNames:
                # search for matches in the keys present in clubs list
                name_matches: list[str] = [key for key, val in self.clubs.items() 
                                           if club_name.lower() in key.lower()]
                if len(name_matches):
                    self.clubNames[club_name] = name_matches[0]
                else:
                    self.clubNames[club_name] = club_name
                    self.clubs[club_name] = Club(club_name, array[-1])

        for key, _ in self.outcastClubNames.items():
            self.clubNames[key] = self.outcastClubNames[key]

        # Now we go over the array once more to add all the transfers
        for array in transfersArray:
            self.addTransfer(array)

        # We sort the transfers in each object
        for _, val in self.clubs.items():
            val.sort()
        for _, val in self.players.items():
            val.sort()
        for _, val in self.seasons.items():
            val.sort()
        self.transfersArray = sorted(self.transfersArray)


    def combineTransfers(self):
        """ This method goes over all the csv files in the ./data directory or the dirName
            directory, and combines their data into a single array to be passed to the 
            createObjects() method.
        """
        transfersArray = []
        listOfFiles: list[str] = []
        dirName: str = self.dirName if self.dirName else "./data"
        for (dirpath, _, filenames) in os.walk(dirName):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames
                                                        if ".csv" in file]
        # mapping from the filename to the country
        countryList = {"dutch_eredivisie.csv" : "Netherlands",
                       "english_championship.csv" : "United Kingdom",
                       "english_premier_league.csv" : "United Kingdom",
                       "french_ligue_1.csv" : "France",
                       "german_bundesliga_1.csv" : "Germany",
                       "italian_serie_a.csv" : "Italy",
                       "portugese_liga_nos.csv" : "Portugal",
                       "russian_premier_liga.csv" : "Russia",
                       "spanish_primera_division.csv" : "Spain"}

        for file in listOfFiles:
            leagueName = file.split("/")[-1]
            countryName = countryList[leagueName]
            with open(file, encoding="utf-8") as file_name:
                reader = csv.reader(file_name, delimiter=',')
                reader.__next__()
                for row in reader: 
                    ## some of the files ommit the period column, we here we add that field
                    if len(row) < 12:
                        row.insert(7, "all-year")
                    ## in some of the rows, the fee entry has a comma in it. so we join
                    #  the two separate parts, and remove the second part 
                    elif len(row) > 12:
                        row[5] = row[5] + "," + row[6]
                        row.remove(6)
                    row.append(countryName)
                    transfersArray.append(row)
        return transfersArray

# improvevments:
# further pruning is needed
#    multiple instances of the same transaction in different files
#       and different ages of the players
#    check the player's age wtf is wrong with this one i
# there are international transactions that can't possibly be detected
