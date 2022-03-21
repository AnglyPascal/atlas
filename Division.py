import os.path, json
import pycountry_convert as pc
from League import League
from Query import Query

class Division:
    """ Object to represent a division of the clubs into groups:
        - First we create a group for all the top 5 clubs from all the 9 major leagues
        - Then we create a group for all the remaining clubs in each league
        - Then we create a group for clubs from each country that has at least 30 clubs 
          outside of these leagues
        - Then we create a group for clubs from each continent

        The groups are stored in a dictionary named self.groups, where the keys are:
        - "club_name" for groups with a single club
        - "league_name others" for groups with remaining clubs from the leagues
        - "country_name others" for groups with remaining clubs from the countries
        - "continent_full_name others" for groups with remaining clubs from the continents
        
        The names of the clubs in each group is stored in a file named groups_of_clubs.json
        If the file exists, we just reuse the values from that file, 
        If it doesn't, we create the data in the else statement.

        The query function transfersBetweenClubs(group_name_1, group_name_2) will return
        all the transfers between the clubs from the two respective groups in an array
        And the function transfersFromToClubs(group_name_1, group_name_2) will return 
        all the transfers that happend from the first group to the next one
    """
    def __init__(self):
        self.leagues = []
        self.data = Query()
        self.clubs = self.data.clubs
        self.clubsMarked = set()
        self.group_names = {}
        self.groups = {}

        if os.path.exists("./groups_of_clubs.json"):
            with open("./groups_of_clubs.json") as f:
                self.group_names = json.load(f)
        else:
            with open("leagues.json") as f:
                league_data = json.load(f)
                for _, url in league_data.items():
                    self.leagues.append(League(url))

            for league in self.leagues:
                for club in league.clubs[:5]:
                    self.group_names[club] = [club]
                self.group_names[league.name + " others"] = league.clubs[5:]
                for club_name in league.clubs:
                    self.clubsMarked.add(club_name)

            # assign the clubs into an dictionary of respective countries 
            countries = {}
            for name, club in self.clubs.items():
                if name not in self.clubsMarked:
                    country = club.country
                    if country not in countries:
                        countries[country] = [name]
                    else:
                        countries[country].append(name)
                    self.clubsMarked.add(name)

            with open("country_outcast_names.json") as file:
                outcasts = json.load(file)
            with open("continent_outcast_names.json") as file:
                outcasts_cont = json.load(file)
            
            continents = {'NA': [], 'SA': [], 'AS': [], 'OC': [], 'AF': [], 'EU': []}
            continents_names = {'NA': 'North America', 'SA': 'South America', 'AS': 'Asia', 
                                'OC': 'Australia', 'AF': 'Africa', 'EU': 'Europe'}
            for country, clubs in countries.items():
                # if that country has more than 30 clubs outside the major leagues, 
                # make a group for it
                if len(clubs) > 30:
                    self.group_names[country + " others"] = clubs
                # if not, insert all the clubs of this country into a dictionary of 
                # the respective continent
                else:
                    cn_name = country if "," not in country \
                                           else country.split(", ")[1] + " " + country.split(",")[0] 
                    if cn_name in outcasts:
                        cn_name = outcasts[cn_name]
                    try:
                        cc = pc.country_name_to_country_alpha2(cn_name, cn_name_format="default")
                        continent_name = pc.country_alpha2_to_continent_code(cc)
                        continents[continent_name].extend(clubs)
                    except KeyError:
                        continent_name = outcasts_cont[cn_name]
                        continents[continent_name].extend(clubs)

            # for each continent, create a group for it
            for continent_code, clubs in continents.items():
                continent_name = continents_names[continent_code]
                self.group_names[continent_name + " others"] = clubs

            # store the data for later use
            with open("./groups_of_clubs.json", 'w') as f:
                json.dump(self.group_names, f)

        for group_name, club_names in self.group_names.items():
            self.groups[group_name] = [self.clubs[club_name] for club_name in club_names]

        for group_name, clubs in self.groups.items():
            for club in clubs:
                for transfer in club.transfers:
                    transfer.group_name = group_name

        self.data.csvTranfers(self.data.transfersArray, "allTransfers.csv")

    def transfersBetweenGroups(self, group_name_1, group_name_2):
        clubs_1 = self.groups[group_name_1]
        clubs_2 = self.groups[group_name_2]
        return self.data.transfersBetweenClubs(clubs_1, clubs_2)

    def transfersFromToGroups(self, group_name_1, group_name_2):
        clubs_1 = self.groups[group_name_1]
        clubs_2 = self.groups[group_name_2]
        return self.data.transfersFromToClubs(clubs_1, clubs_2)

if __name__ == "__main__":
    div = Division()
    # print(len(div.nodes))
    
    for _, n in div.groups.items():
        # ss = [club.__str__() for club in node]
        print(len(n))
