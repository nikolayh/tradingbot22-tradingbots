from requests import get, post, put
from urllib.parse import quote_plus

class BaseBot:

    def __init__(self, name: str, backendurl: str = "http://127.0.0.1:8000"):
        self.backendurl: str = backendurl
        self.headers: dict = { 'accept': 'application/json', 'Content-Type': 'application/json'}
        self.name: str = self.checkOrCreate(name)
    
    def checkOrCreate(self, name: str) -> str:
        response = get(self.backendurl + '/bot/' + quote_plus(name), headers=self.headers)
        if response.status_code != 200:
            # create
            json_data = {
                'name': name,
                'description': 'created in basebot',
            }
            response = put(self.backendurl + "/bot", json=json_data, headers=self.headers)
        return name

    def getPortfolio(self) -> dict:
        response = get(self.backendurl + '/bot/' + quote_plus(self.name), headers=self.headers)
        if response.status_code != 200:
            raise Exception("Error getting portfolio: ", response.text)
        return response.json()["portfolio"]

    def getPortfolioWorth(self) -> float:
        response = get(self.backendurl + '/bot/%s/portfolioworth' % quote_plus(self.name), headers=self.headers)
        if response.status_code != 200:
            raise Exception("Error getting portfolio worth: ", response.text)
        return response.json()["worth"]

    def buy(self, ticker: str, amount: float = -1, amountInUSD: bool = False):
        params = {
            "botname": self.name,
            'ticker': ticker,
            'amount': amount,
            "amountInUSD": amountInUSD,
        }
        response = put(self.backendurl + '/buy/', params=params, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Error buying: ", response.text)

    def sell(self, ticker: str, amount: float = -1, amountInUSD: bool = False):
        params = {
            "botname": self.name,
            'ticker': ticker,
            'amount': amount,
            "amountInUSD": amountInUSD,
        }
        response = put(self.backendurl + '/sell/', params=params, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Error selling: ", response.text)

if __name__ == "__main__":
    bot = BaseBot("testbot")
    print(bot.getPortfolio())
    bot.buy("AAPL", 2000, amountInUSD=True)
    print("portfolio after buy")
    print(bot.getPortfolio())
    print("portfolio after sell")
    bot.sell("AAPL", 1500, amountInUSD=True)
    print(bot.getPortfolio())
    print("portfolio worth is: %.2f dollars" % bot.getPortfolioWorth())