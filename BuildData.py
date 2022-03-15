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
        self.transfersArray: list[list[str]] = []
        self.dirName = dirName

        self.combineTransfers()
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

        transfer = Transfer(fromClub, toClub, player, fee, season, period, isLoan)
        fromClub.addTransfer(transfer)
        toClub.addTransfer(transfer)
        player.addTransfer(transfer)
        season.addTransfer(transfer)

    def createObjects(self):
        for array in self.transfersArray:
            club_name: str = array[0]
            if club_name not in self.clubNames:
                self.clubNames[club_name] = club_name
                self.clubs[club_name] = Club(club_name)

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

        for array in self.transfersArray:
            club_name: str = array[4]
            if club_name not in self.clubNames:
                name_matches: list[str] = [key for key, val in self.clubs.items() 
                                           if club_name.lower() in key.lower()]
                if len(name_matches):
                    self.clubNames[club_name] = name_matches[0]
                else:
                    self.clubNames[club_name] = club_name
                    self.clubs[club_name] = Club(club_name)

        outcastClubNames = {
            "Barcelona" : "FC Barcelona",
            "Admira/Wacker" : "Admira Wacker",
        }

        for key, _ in outcastClubNames.items():
            self.clubNames[key] = outcastClubNames[key]

        for array in self.transfersArray:
            self.addTransfer(array)

        for _, val in self.clubs.items():
            val.sort()
        for _, val in self.players.items():
            val.sort()
        for _, val in self.seasons.items():
            val.sort()


    def combineTransfers(self):
        listOfFiles: list[str] = []
        dirName: str = self.dirName if self.dirName else "./data"
        for (dirpath, _, filenames) in os.walk(dirName):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]

        for file in listOfFiles:
            with open(file, encoding="utf-8") as file_name:
                reader = csv.reader(file_name, delimiter=',')
                reader.__next__()
                for row in reader: 
                    if len(row) < 12:
                        row.insert(7, "all-year")
                    elif len(row) > 12:
                        row[5] = row[5] + "," + row[6]
                        row.remove(6)
                    self.transfersArray.append(row)

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

    def csv(self, club_name: str = None, player_name: str = None, season: str = None):
        filteredTransfersArray: list[Transfer] = self.filter(club_name, player_name, season)
        fileName: str = "allTransfers" + ("_"+club_name if club_name else "") + \
                                         ("_"+player_name if player_name else "") + \
                                         ("_"+season if season else "") + ".csv"
        arrayToPrint = [["from club", "to club", "player name", "age", "position", "fee", 
                         "transfer type", "period", "year", "season"]]
        arrayToPrint.extend([tf.toArray() for tf in filteredTransfersArray]) 
        with open(fileName, 'w', newline='') as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(arrayToPrint)




if __name__ == "__main__":
    bd = BuildData()
    bd.csv(club_name = "Admira Wacker")
    # with open("clubNames.json", 'w', encoding="utf-8") as f:
    #     json.dump(bd.clubNames, f, ensure_ascii=False)



# improvevments:
# add count, write query code, write graph code
# output in csv
