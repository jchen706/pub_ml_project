"""

"""
class AF():
  def __init__(self,year):
    self.year = year
    self.net_income = None
    self.total_revenue = None
    self.net_loss = None
    self.gross_profit = None
    self.income_before_taxes = None
    self.cost_of_revenue = None
    self.ebit = None
    self.total_assets = None
    self.total_liabilities = None
  
  
  def __str__(self):
    return self.year

"""

"""
class Company:
  def __init__(self,company_name, ticker, exchange, ipo_price, number_of_shares, dollar_value_of_shares, date, href):
    self.name = company_name
    self.ticker = ticker 
    self.exchange = exchange
    self.ipo_price = ipo_price
    self.number_of_shares = number_of_shares
    self.dollar_value_of_shares = dollar_value_of_shares
    self.date = date
    self.valuation = None
    self.revenue_growth = None
    self.href = href

    # list of AF
    self.financials = []

    # list of tuple (trading day, price)
    self.five_trading_day_prices = []


    # need to be extraced from S-1 seems like it
    
  def toListPartOne(self):
    return [self.name, self.ticker, self.exchange, self.ipo_price, self.number_of_shares, self.dollar_value_of_shares, self.date, self.href]

  

  def __str__(self):
    return self.name

