import csv
from BuildData import BuildData
from Transfer import Transfer
# from Club import Club
# from Player import Player
# from Season import Season


class Query:
    def __init__(self):
        self.data = BuildData()
        self.clubs = self.data.clubs
        self.players = self.data.players
        self.seasons = self.data.seasons
        self.clubNames = self.data.clubNames
        self.transfersArray = self.data.transfersArray
        self.dirName = self.data.dirName

    def filter(self, club_name: str = None, player_name: str = None, season: str = None):
        """ Filter the list of transfers based on the query
        """
        if not club_name and not player_name and not season:
            return self.transfersArray
        if club_name:
            return [tf for tf in self.clubs[self.clubNames[club_name]].transfers 
                    if (player_name and not season and tf.player.name == player_name) or 
                       (season and not player_name and tf.season.season == season) or 
                       (season and player_name and tf.player.name == player_name and 
                        tf.season.season == season)]
        if player_name:
            return [tf for tf in self.players[player_name].transfers
                    if (season and tf.season.season == season)]
        if season:
            return list(tf for tf in self.seasons[season].transfers)

        return []

    def csvFiltered(self, club_name: str = None, player_name: str = None, season: str = None):
        """ Write the results of a filtering into a csv file with appropriate filenames """
        filteredTransfersArray: list[Transfer] = self.filter(club_name, player_name, season)
        fileName: str = "allTransfers" + ("_"+club_name if club_name else "") + \
                                         ("_"+player_name if player_name else "") + \
                                         ("_"+"_".join(season.split("/")) if season else "") + \
                                         ".csv"
        self.csv(filteredTransfersArray, fileName)

    def csvMostTransferred(self, num):
        """ Find the num most transferred players """
        playersArray = self.mostTransferredPlayers(num)
        array = []
        for player in playersArray:
            array += player.transfers
        fileName = "most transfererred players.csv"
        self.csv(array, fileName)

    def csvMostValuable(self, num):
        """ Find the num most transferred players """
        playersArray = self.mostValuablePlayers(num)
        array = []
        for player in playersArray:
            array += [tf for tf in player.transfers if tf.fee != 0]
        fileName = "most valuable players.csv"
        self.csv(array, fileName)

    def csv(self, array: list[Transfer], fileName: str):
        """ Given an array of Transfer objects and a filename,
            write the array contents into a csv file
        """
        arrayToPrint = [["from club", "to club", "league", "player name", "age", "position", "fee",
                         "transfer type", "period", "year", "season", "tranfer between"]]
        arrayToPrint.extend([tf.toArray() for tf in array])
        with open(fileName, 'w', newline='') as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(arrayToPrint)

    def mostTransferredPlayers(self, num: int):
        playersList = [val for key, val in self.players.items()]
        playersList = sorted(playersList,
                             key = lambda tf: tf.num_of_transfers(),
                             reverse = True)[:num]
        return playersList

    def mostValuablePlayers(self, num: int):
        playersList = [val for key, val in self.players.items()]
        playersList = sorted(playersList,
                             key = lambda tf: tf.value_with_loan,
                             reverse = True)[:num]
        return playersList

if __name__ == "__main__":
    data = Query()
    # data.csvFiltered(club_name   = "Barcelona", 
    #                  season      = "2019/2020", 
    #                  player_name = "Philippe Coutinho")
    # print(data.players["Philippe Coutinho"].value)
    data.csvMostValuable(20)

    # with open("clubNames.json", 'w', encoding="utf-8") as f:
    #     json.dump(bd.clubNames, f, ensure_ascii=False)

