from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import unidecode
import Transferable

class Club(Transferable.Transferable):
    def __init__(self, name, country, league, total_market_value, 
                 squad_size, average_age, nat_team_players):
        super().__init__()
        self.name = name
        self.country = country
        self.league = league
        self.squad_size = squad_size
        self.average_age = average_age
        self.nat_team_players = nat_team_players
        self.total_market_value = total_market_value

    @classmethod
    def fetchFromURL(cls, name):
        country = "" 
        league = ""
        squad_size = ""
        average_age = ""
        nat_team_players = ""
        total_market_value = ""

        search_url = "https://www.transfermarkt.co.uk/schnellsuche/ergebnis/schnellsuche?query=" + \
                     "+".join(name.split(" "))
        try:
            req = Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')
        except UnicodeEncodeError:
            search_url_unaccented = unidecode.unidecode(search_url)
            req = Request(search_url_unaccented, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')

        try:
            rows = soup.find_all("div", {"class": "row"})[1:]
            row = None
            for row_ in rows:
                try:
                    row_text = row_.find("div", {"class": "table-header"}).text
                    if "Search results: Clubs" in row_text:
                        row = row_
                except AttributeError:
                    pass
            if not row:
                raise AttributeError

            tdtable = row.find("table", {"class": "inline-table"})
            td = tdtable.find("td", {"class": "hauptlink"})

            club_url = "https://www.transfermarkt.co.uk" + td.find("a")["href"]
            req = Request(club_url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')

            try:
                country = row.find("img", {"class": "flaggenrahmen"})["alt"]
                league = soup.find("a", {"class": "hervorgehobener_link"}).text
            except AttributeError:
                pass

            try:
                dataVals = soup.find_all("span", {"class": "dataValue"})
                squad_size = dataVals[0].text.strip()
                average_age = dataVals[1].text.strip()
                nat_team_players = dataVals[2].a.text.strip()
            except (IndexError, AttributeError):
                pass

            try:
                tmv = soup.find("div", {"class": "dataMarktwert"})
                tmv.span.extract()
                tmv.span.extract()
                tmv.p.extract()
                total_market_value = tmv.text.strip()
            except AttributeError:
                pass
        except (TypeError, AttributeError):
            pass
        return cls(name, country, league, total_market_value, 
                   squad_size, average_age, nat_team_players)

    def __str__(self):
        return self.name
        # return "name: " + self.name + "\ncountry: " + self.country + "\nleague: " + self.league

    def __lt__(self, other):
        return self.name < other.name

    def toArray(self):
        return [self.name, self.country, self.league, self.total_market_value, 
                self.squad_size, self.average_age, self.nat_team_players]


if __name__ == "__main__":
    club = Club.fetchFromURL("Barcelona")
    print(club.toArray())
