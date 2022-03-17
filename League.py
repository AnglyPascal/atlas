from urllib.request import Request, urlopen
from json import load
from bs4 import BeautifulSoup

class League:
    def __init__(self, league_url):
        self.league_url = league_url
        self.clubs, self.name, self.country = self.getClubs()

    def getClubs(self):
        req = Request(self.league_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        tds = soup.find_all("td", {"class": "zentriert no-border-rechts"})
        clubs = []
        for td in tds:
            links = td.find_all("a")
            for link in links:
                clubs.append(link["title"])
        name = soup.find("h1", {"class": "spielername-profil"}).text
        country = soup.find("img", {"class": "flaggenrahmen"})["title"]
        return (clubs, name, country)
    
    def __str__(self):
        return "League name: " + self.name + "\n" + \
               "Country of origin: " + self.country + "\n" + \
               "Top 5 clubs: " + ", ".join(self.clubs[:5])

class TopClubs:
    def __init__(self):
        with open("special_players.json", 'r') as file:
            leagueLinks = load(file)
        self.leagues: list[League] = []
        for _, url in leagueLinks.items():
            self.leagues.append(League(url))


if __name__ == "__main__":
    league = League("https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1")
    print(league)
