from bsedata.bse import BSE

bse = BSE(update_codes = True)

class StockAPI:
    def __init__(self, stock) -> None:
        self.stock = stock
        self.quote = bse.getQuote(self.stock.scrip_code)

    def get_price(self):
        return self.quote["currentPrice"]

    def get_company_name(self):
        return self.quote["companyName"]
