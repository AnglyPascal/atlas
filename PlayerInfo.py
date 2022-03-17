from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

class PlayerInfo:
    def __init__(self, player_url):
        self.player_url = player_url

        req = Request(self.player_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all("tr", {"class": "zeile-transfer"})
        # print(trs)

        self.name = soup.find("meta", {"property": "og:title"})["content"].split("-")[0]

        self.transfers = []
        for tr in trs:
            arr = []

            cs = tr.find_all("td", {"class": "no-border-rechts vereinswappen"})
            fromClub = cs[0].find("a")["title"]
            toClub   = cs[1].find("a")["title"]

            infos = tr.find_all("td", {"class": "zentriert"})
            season = "/".join(["20" + yr for yr in infos[0].text.split("/")])
            date = infos[1].text
            market_value = tr.find("td", {"class": "zelle-mw"}).text[1:-1]
            fee_text = tr.find("td", {"class": "zelle-abloese"}).text
            loan = "loan" in fee_text or "Loan" in fee_text
            try:
                fee = float(fee_text[1:-1])
            except ValueError:
                fee = 0

            transfer_url = "https://www.transfermarkt.com" + infos[-1].find("a")["href"]
            req_tr = Request(transfer_url, headers={'User-Agent': 'Mozilla/5.0'})
            html_tr = urlopen(req_tr).read()
            div_tr = BeautifulSoup(html_tr, 'html.parser').find("div", {"class": "large-4 columns"})
            tds = [td for td in div_tr.find_all("td", {"class": "zentriert"})
                      if "Age at time of transfer" in td.text]
            tds[0].br.extract()
            tds[0].b.extract()
            age = tds[0].text.strip().split(" ")[0]

            arr = [fromClub, toClub, age, fee, loan, season, date, market_value]
            self.transfers.append(arr)

    def __str__(self):
        return "Player name: " + self.name + "\n" + \
               "Transfers: \n"+"\n".join([", ".join([str(x) for x in tr]) for tr in self.transfers])

# class SpecialPlayers:


if __name__ == "__main__":
    player = PlayerInfo("https://www.transfermarkt.com/lionel-messi/profil/spieler/28003")
    # print(player.transfers)
    print(player)
