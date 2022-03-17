import csv, pickle, json
from os.path import exists
import resource, sys
from BuildData import BuildData
from Transfer import Transfer
# from League import League, TopClubs

# we need this part to raise the stack size to allow pickling to happen
max_rec = 0x100000
# May segfault without this line. 0x100 is a guess at the size of each stack frame.
resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
sys.setrecursionlimit(max_rec)

class Query:
    def __init__(self, renew = False):
        """ We pickle the data if it's already computed so as to avoid redoing a lot of work.
            We can force this method to recompute all the data by setting renew to True.
        """
        if not renew and exists("./stored_compiled_data_obj"):
            try:
                with open("./stored_compiled_data_obj", 'rb') as data_file:
                    self.data = pickle.load(data_file)
            except TypeError:
                self.data = BuildData()
                with open("./stored_compiled_data_obj", 'wb') as data_file:
                    pickle.dump(self.data, data_file)
        else:
            # if pickling is not desired, removing this block by 
            # this single line will do the job
            self.data = BuildData() 
            with open("./stored_compiled_data_obj", 'wb') as data_file:
                pickle.dump(self.data, data_file)

        # creating pointers to the data structure fields
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
        self.csvTranfers(filteredTransfersArray, fileName)

    def csv(sself, arrayToPrint, fileName):
        with open("./compiled_data/" + fileName, 'w', newline='') as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(arrayToPrint)

    def csvTranfers(self, array: list[Transfer], fileName: str):
        """ Given an array of Transfer objects and a filename,
            write the array contents into a csv file
        """
        arrayToPrint = [["from club", "to club", "league", "player name", "age", "position", "fee",
                         "transfer type", "period", "year", "season", "tranfer between"]]
        arrayToPrint.extend([tf.toArray() for tf in array])
        self.csv(arrayToPrint, fileName)

    def mostTransferredPlayers(self, num: int):
        """ Find the num most transferred players """

        playersList = [val for key, val in self.players.items()]
        playersList = sorted(playersList,
                             key = lambda tf: tf.num_of_transfers(),
                             reverse = True)[:num]
        array = []
        for player in playersList:
            array += player.transfers
        fileName = "./compiled_data/most transfererred players.csv"
        self.csvTranfers(array, fileName)

    def mostValuablePlayers(self, num: int):
        """ Find the num most valued players """
        playersList = [val for key, val in self.players.items()]
        playersList = sorted(playersList,
                             key = lambda tf: tf.value_with_loan,
                             reverse = True)[:num]
        array = []
        for player in playersList:
            array += [tf for tf in player.transfers if tf.fee != 0]
        fileName = "./compiled_data/most valuable players.csv"
        self.csvTranfers(array, fileName)

    def mostExpensiveTranfers(self, num: int):
        """ Find the num most expensive transactions """
        transfersList = sorted(self.transfersArray,
                             key = lambda tf: tf.fee,
                             reverse = True)[:num]
        fileName = "./compiled_data/most expensive transfers.csv"
        self.csvTranfers(transfersList, fileName)


    def transfersBetweenClubs(self, clubs1_name: str, clubs2_name: str) -> list[Transfer]:
        """ Given two sets of clubs, returns the list of transfers 
            that happend one set to another in either direction
        """
        clubs1 = [self.data.getClub(club1_name) for club1_name in clubs1_name]
        clubs2 = [self.data.getClub(club2_name) for club2_name in clubs2_name]
        allTransfers = []
        for club in clubs1:
            allTransfers.extend(club.transfers)
        transfers = [tf for tf in allTransfers if (tf.fromClub in clubs2) or (tf.toClub in clubs2)]
        return transfers

    def csvTransfersBetweenClubs(self, clubs1_name, clubs2_name):
        """ Print the transfers """
        transfers = self.transfersBetweenClubs(clubs1_name, clubs2_name)
        fileName = "transfers between (" + ", ".join(clubs1_name) + \
            ") and (" + ", ".join(clubs2_name) + ").csv"
        self.csvTranfers(transfers, fileName)

    def weightOfTransfersBetweenClubs(self, clubs1_name, clubs2_name, withLoan = False):
        """ Find the total amount of transfers that happend between the two sets of clubs """
        transfers = self.transfersBetweenClubs(clubs1_name, clubs2_name)
        weight = 0
        for tr in transfers:
            weight += (tr.fee if not tr.isLoan or withLoan else 0)
        return weight


    def transfersFromToClubs(self, clubs1_name: str, clubs2_name: str) -> list[Transfer]:
        """ Given two sets of clubs, returns the list of transfers 
            that happend from set1 to set2. Used to make the directed graph
        """
        clubs1 = [self.data.getClub(club1_name) for club1_name in clubs1_name]
        clubs2 = [self.data.getClub(club2_name) for club2_name in clubs2_name]
        allTransfers = []
        for club in clubs1:
            allTransfers.extend(club.transfers)
        transfers = [tf for tf in allTransfers if (tf.fromClub in clubs1) and (tf.toClub in clubs2)]
        return transfers

    def weightOfTransfersFromToClubs(self, clubs1_name, clubs2_name, withLoan = False):
        """ Given two sets of clubs, returns the total amount of transfers 
            that happend from set1 to set2. Used to make the directed graph
        """
        transfers = self.transfersBetweenClubs(clubs1_name, clubs2_name)
        weight = 0
        for tr in transfers:
            weight += (tr.fee if not tr.isLoan or withLoan else 0)
        return weight

    def clubList(self):
        array = [["Club name", "Country", "League", "Total Market Value (in M)",
                  "Squad size", "Average age", "Number of national team players"]]
        for _, club in self.clubs.items():
            array.append(club.toArray())
        fileName = "clubs_list.csv"
        self.csv(array, fileName)


if __name__ == "__main__":
    data = Query(True)
    # data.csvTransfersBetweenClubs(["Ajax Amsterdam"], ["Barcelona"])
    data.clubList()

    with open("clubNames.json", 'w', encoding="utf-8") as f:
        json.dump(data.clubNames, f, ensure_ascii=False)
