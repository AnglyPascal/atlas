import os
import csv
# import json
from typing import Dict
from Transfer import Transfer
from Club import Club
from Player import Player
from Season import Season

class BuildData:
    def __init__(self, dirName: str = None):
        self.clubs: Dict[str, Club] = {}
        self.clubNames: Dict[str, str] = {}
        self.players: Dict[str, Player] = {}
        self.seasons: Dict[str, Season] = {}
        self.transfersArray = set()
        self.dirName = dirName

        self.createObjects()

    def getClub(self, name) -> Club:
        return self.clubs[self.clubNames[name]]

    def getPlayer(self, name) -> Player:
        return self.players[name]

    def getSeason(self, season) -> Season:
        return self.seasons[season]

    def addTransfer(self, array: list[str]):
        fromClub: Club = self.getClub(array[4]) if array[6] == "in" else self.getClub(array[0])
        toClub: Club   = self.getClub(array[0]) if array[6] == "in" else self.getClub(array[4])
        player: Player = self.getPlayer(array[1])
        season: Season = self.getSeason(array[11])
        try:
            fee: float = float(array[8])
        except ValueError:
            fee: float = 0
        isLoan: bool = "loan" in array[5] or "Loan" in array[5]
        period: str = array[7]
        league: str = array[9]

        transfer = Transfer(fromClub, toClub, player, fee, season, period, isLoan, league)
        fromClub.addTransfer(transfer)
        toClub.addTransfer(transfer)
        player.addTransfer(transfer)
        season.addTransfer(transfer)
        self.transfersArray.add(transfer)


    def createObjects(self):
        transfersArray = self.combineTransfers()
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

        for array in transfersArray:
            club_name: str = array[4]
            if club_name not in self.clubNames:
                name_matches: list[str] = [key for key, val in self.clubs.items() 
                                           if club_name.lower() in key.lower()]
                if len(name_matches):
                    self.clubNames[club_name] = name_matches[0]
                else:
                    self.clubNames[club_name] = club_name
                    self.clubs[club_name] = Club(club_name, array[-1])

        outcastClubNames = {
            "Barcelona" : "FC Barcelona",
            "Admira/Wacker" : "Admira Wacker",
        }

        for key, _ in outcastClubNames.items():
            self.clubNames[key] = outcastClubNames[key]

        for array in transfersArray:
            self.addTransfer(array)

        for _, val in self.clubs.items():
            val.sort()
        for _, val in self.players.items():
            val.sort()
        for _, val in self.seasons.items():
            val.sort()
        self.transfersArray = sorted(self.transfersArray)

    def combineTransfers(self):
        transfersArray = []
        listOfFiles: list[str] = []
        dirName: str = self.dirName if self.dirName else "./data"
        for (dirpath, _, filenames) in os.walk(dirName):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]

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
                    if len(row) < 12:
                        row.insert(7, "all-year")
                    elif len(row) > 12:
                        row[5] = row[5] + "," + row[6]
                        row.remove(6)
                    row.append(countryName)
                    transfersArray.append(row)
        return transfersArray

    def filter(self, club_name: str = None, player_name: str = None, season: str = None):
        if not club_name and not player_name and not season:
            return self.transfersArray
        if club_name:
            return self.clubs[self.clubNames[club_name]].transfers
        if player_name:
            return self.players[player_name].transfers
        if season:
            return self.seasons[season].transfers

        # add some mixed filtering
        return []

    def csvFiltered(self, club_name: str = None, player_name: str = None, season: str = None):
        filteredTransfersArray: list[Transfer] = self.filter(club_name, player_name, season)
        fileName: str = "allTransfers" + ("_"+club_name if club_name else "") + \
                                         ("_"+player_name if player_name else "") + \
                                         ("_"+season if season else "") + ".csv"
        self.csv(filteredTransfersArray, fileName)

    def csvMostTransferred(self, num):
        playersArray = self.mostTransferredPlayers(num)
        array = []
        for player in playersArray:
            array += player.transfers
        fileName = "most transfererred players.csv"
        self.csv(array, fileName)

    def csv(self, array: list[Transfer], fileName: str):
        arrayToPrint = [["from club", "to club", "league", "player name", "age", "position", "fee", 
                         "transfer type", "period", "year", "season", "tranfer between"]]
        arrayToPrint.extend([tf.toArray() for tf in array]) 
        with open(fileName, 'w', newline='') as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(arrayToPrint)

    def mostTransferredPlayers(self, num: int):
        playersList = [val for key, val in self.players.items()]
        playersList = sorted(playersList, 
                             key = lambda tf: tf.num_of_transfers, 
                             reverse = True)[:num]
        return playersList

if __name__ == "__main__":
    bd = BuildData()
    # bd.csvFiltered(club_name = "Admira Wacker")
    bd.csvMostTransferred(20)
    # bd.csv()
    # with open("clubNames.json", 'w', encoding="utf-8") as f:
    #     json.dump(bd.clubNames, f, ensure_ascii=False)



# improvevments:
# further pruning is needed
#    multiple instances of the same transaction in different files
#       and different ages of the players
#    add a new field country in the clubs based on the filename also the league
#       and indicate whethere the transaction was international or local
#    check the player's age
#   
# output in csv
