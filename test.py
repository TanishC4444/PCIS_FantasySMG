import yfinance as yf

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    
    # Basic Info
    info = stock.info
    print(f"--- {info['shortName']} ({ticker}) ---")
    print(f"Current Price: ${info['currentPrice']}")
    print(f"Market Cap: ${info['marketCap']:,}")
    print(f"P/E Ratio: {info.get('trailingPE', 'N/A')}")
    print(f"EPS: {info.get('trailingEps', 'N/A')}")
    print(f"Dividend Yield: {info.get('dividendYield', 'N/A') * 100 if info.get('dividendYield') else 'N/A'}%")
    print(f"52-Week Range: {info['fiftyTwoWeekLow']} - {info['fiftyTwoWeekHigh']}")
    print(f"Beta: {info.get('beta', 'N/A')}")

    # Financials (Revenue, Net Income)
    financials = stock.financials
    print("\n--- Financial Data ---")
    print(financials.loc[['Total Revenue', 'Net Income'], :])

    # Recent News
    print("\n--- Latest News ---")
    for article in stock.news[:3]:
        print(f"{article['title']} - {article['publisher']}")
        print(article['link'])
        print()

# Example Usage
ticker_symbol = input("Enter Stock Ticker Symbol: ").upper()
get_stock_data(ticker_symbol)
