import os
import threading
import webbrowser
import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Use environment variables for file paths with fallbacks
USER_DATA_FILE = os.environ.get('USER_DATA_FILE', "users.csv")
SOLD_DATA_FILE = os.environ.get('SOLD_DATA_FILE', "sold.csv")
STARTING_BALANCE = float(os.environ.get('STARTING_BALANCE', 100000.00))

# Ensure user data file exists
if not os.path.exists(USER_DATA_FILE) or os.stat(USER_DATA_FILE).st_size == 0:
    df = pd.DataFrame(columns=["Ticker", "Date Bought", "Quantity", "Price Bought", "Current Value", "Earnings", "Change %", "Status"])
    df.to_csv(USER_DATA_FILE, index=False)
    with open("balance.txt", "w") as f:
        f.write(str(STARTING_BALANCE))

if not os.path.exists(SOLD_DATA_FILE):
    pd.DataFrame(columns=["Ticker", "Date Bought", "Quantity", "Price Bought", "Sell Price", "Profit", "Sell Date"]).to_csv(SOLD_DATA_FILE, index=False)
    

# Function to get balance
def get_balance():
    if not os.path.exists("balance.txt"):
        with open("balance.txt", "w") as f:
            f.write(str(STARTING_BALANCE))
    with open("balance.txt", "r") as f:
        return float(f.read())

# Function to update balance
def update_balance(amount):
    balance = get_balance() + amount
    with open("balance.txt", "w") as f:
        f.write(str(balance))
    return balance

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/practice')
def practice():
    return render_template('practice.html')

@app.route('/learn')  # Added route for learn.html
def learn():
    return render_template('learn.html')

@app.route('/balance', methods=['GET'])
def balance():
    return jsonify({"balance": get_balance()})

@app.route('/stock', methods=['GET'])
def get_stock_data():
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        return jsonify({"error": "Missing ticker"}), 400

    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d", interval="5m")

    if hist.empty:
        return jsonify({"error": "Invalid ticker or no data available"}), 400

    timestamps = hist.index.strftime('%H:%M').tolist()
    prices = hist['Close'].round(2).tolist()
    stock_info = stock.info

    extra_data = {
        "Previous Close": stock_info.get("previousClose"),
        "Open": stock_info.get("open"),
        "Day High": stock_info.get("dayHigh"),
        "Day Low": stock_info.get("dayLow"),
        "Beta": stock_info.get("beta"),
        "52-Week High": stock_info.get("fiftyTwoWeekHigh"),
        "52-Week Low": stock_info.get("fiftyTwoWeekLow"),
        "Market Cap": stock_info.get("marketCap"),
        "Volume": stock_info.get("volume"),
        "Avg Volume": stock_info.get("averageVolume"),
    }

    return jsonify({"timestamps": timestamps, "prices": prices, "extra_data": extra_data})

@app.route('/get_trades', methods=['GET'])
def get_trades():
    if not os.path.exists(USER_DATA_FILE) or os.stat(USER_DATA_FILE).st_size == 0:
        return jsonify([])

    df = pd.read_csv(USER_DATA_FILE)

    # Round all numerical values
    df["Price Bought"] = df["Price Bought"].round(2)
    df["Current Value"] = df["Current Value"].round(2)
    df["Earnings"] = df["Earnings"].round(2)
    df["Change %"] = df["Change %"].round(2)

    trades = df.to_dict(orient="records")  
    return jsonify(trades)

@app.route('/trade', methods=['GET'])
def trade_stock():
    ticker = request.args.get('ticker', '').upper()
    quantity = int(request.args.get('quantity', 0))
    trade_type = request.args.get('type', '').lower()

    if not ticker or quantity <= 0 or trade_type not in ['buy', 'sell']:
        return jsonify({"error": "Invalid trade parameters"}), 400

    stock = yf.Ticker(ticker)
    current_price = round(stock.history(period="1d", interval="1m").iloc[-1]['Close'], 2)
    total_cost = round(quantity * current_price, 2)

    df = pd.read_csv(USER_DATA_FILE)

    if trade_type == "buy":
        balance = get_balance()
        if total_cost > balance:
            return jsonify({"error": "Insufficient funds"}), 400

        new_trade = pd.DataFrame({
            "Ticker": [ticker], 
            "Date Bought": [datetime.now().strftime('%Y-%m-%d %H:%M')],
            "Quantity": [quantity], 
            "Price Bought": [current_price], 
            "Current Value": [total_cost],
            "Earnings": [0], 
            "Change %": [0], 
            "Status": ["OWNED"]
        })
        df = pd.concat([df, new_trade], ignore_index=True)
        update_balance(-total_cost)

    elif trade_type == "sell":
        stock_rows = df[(df["Ticker"] == ticker) & (df["Quantity"] > 0)]

        if stock_rows.empty:
            return jsonify({"error": "No shares available to sell"}), 400

        stock_row = stock_rows.iloc[0]  
        buy_price = stock_row["Price Bought"]
        profit = (current_price - buy_price) * quantity

        # Save sale to sold.csv
        sold_df = pd.read_csv(SOLD_DATA_FILE)
        new_sale = pd.DataFrame({
            "Ticker": [ticker], 
            "Date Bought": [stock_row["Date Bought"]],
            "Quantity": [quantity], 
            "Price Bought": [buy_price], 
            "Sell Price": [current_price],
            "Profit": [profit],
            "Sell Date": [datetime.now().strftime('%Y-%m-%d %H:%M')]
        })
        sold_df = pd.concat([sold_df, new_sale], ignore_index=True)
        sold_df.to_csv(SOLD_DATA_FILE, index=False)

        # Remove sold stocks from users.csv
        df = df[df["Ticker"] != ticker]
        update_balance(total_cost)

    df.to_csv(USER_DATA_FILE, index=False)
    return jsonify({"success": f"{trade_type.capitalize()} {quantity} shares of {ticker} at ${current_price:.2f}", "balance": get_balance()})

@app.route('/reset', methods=['GET'])
def reset_account():
    df = pd.DataFrame(columns=["Ticker", "Date Bought", "Quantity", "Price Bought", "Current Value", "Earnings", "Change %", "Status"])
    df.to_csv(USER_DATA_FILE, index=False)
    with open("balance.txt", "w") as f:
        f.write(str(STARTING_BALANCE))
    return jsonify({"success": "Account reset successfully", "balance": STARTING_BALANCE})

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
