import yfinance as yf

# Define the ticker symbol for the stock you want to fetch
symbol = "AAPL"  # Example: Apple Inc.
stock = yf.Ticker(symbol)
info = stock.info
print(info)
