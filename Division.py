import json
import pycountry_convert as pc
from League import League
from Query import Query
from Club import Club

class Division:
    def __init__(self):
        self.leagues = []
        self.data = Query()
        self.clubs = self.data.clubs
        self.clubsMarked = set()

        with open("leagues.json") as f:
            league_data = json.load(f)
            for _, url in league_data.items():
                self.leagues.append(League(url))

        self.nodes: list[Club] = []
        for league in self.leagues:
            self.nodes.extend([[club] for club in league.clubs[:5]])
            self.nodes.append([self.clubs[club_name] for club_name in league.clubs[5:]])
            for club_name in league.clubs:
                self.clubsMarked.add(club_name)

        countries = {}
        for name, club in self.clubs.items():
            if name not in self.clubsMarked:
                country = club.country
                if country not in countries:
                    countries[country] = [club]
                else:
                    countries[country].append(club)
                self.clubsMarked.add(name)

        with open("country_outcast_names.json") as file:
            outcasts = json.load(file)
        with open("continent_outcast_names.json") as file:
            outcasts_cont = json.load(file)
        
        
        continents = {'NA': [], 'SA': [], 'AS': [], 'OC': [], 'AF': [], 'EU': []}
        for country, clubs in countries.items():
            if len(clubs) > 30:
                self.nodes.append(clubs)
            else:
                country_name = country if "," not in country \
                                       else country.split(", ")[1] + " " + country.split(",")[0] 
                if country_name in outcasts:
                    country_name = outcasts[country_name]
                try:
                    cc = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
                    continent_name = pc.country_alpha2_to_continent_code(cc)
                    continents[continent_name].extend(clubs)
                except KeyError:
                    continent_name = outcasts_cont[country_name]
                    continents[continent_name].extend(clubs)
        for _, clubs in continents.items():
            self.nodes.append(clubs)

if __name__ == "__main__":
    div = Division()
    # print(len(div.nodes))
    
    for node in div.nodes:
        # ss = [club.__str__() for club in node]
        print(len(node))
