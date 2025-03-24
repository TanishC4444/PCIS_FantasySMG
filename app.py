import os
import threading
import webbrowser
import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

USER_DATA_FILE = "users.csv"
STARTING_BALANCE = 100000.00  # Initial balance

# Ensure user data file exists
if not os.path.exists(USER_DATA_FILE) or os.stat(USER_DATA_FILE).st_size == 0:
    df = pd.DataFrame(columns=["Ticker", "Date Bought", "Quantity", "Price Bought", "Current Value", "Earnings", "Change %", "Status"])
    df.to_csv(USER_DATA_FILE, index=False)
    with open("balance.txt", "w") as f:
        f.write(str(STARTING_BALANCE))

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

@app.route('/trade', methods=['GET'])
def trade_stock():
    ticker = request.args.get('ticker', '').upper()
    quantity = int(request.args.get('quantity', 0))
    trade_type = request.args.get('type', '').lower()

    if not ticker or quantity <= 0 or trade_type not in ['buy', 'sell']:
        return jsonify({"error": "Invalid trade parameters"}), 400

    stock = yf.Ticker(ticker)
    current_price = stock.history(period="1d", interval="1m").iloc[-1]['Close']
    total_cost = quantity * current_price

    balance = get_balance()
    if trade_type == "buy" and total_cost > balance:
        return jsonify({"error": "Insufficient funds"}), 400

    df = pd.read_csv(USER_DATA_FILE)
    new_trade = pd.DataFrame({
        "Ticker": [ticker], "Date Bought": [datetime.now().strftime('%Y-%m-%d %H:%M')],
        "Quantity": [quantity], "Price Bought": [current_price], "Current Value": [current_price * quantity],
        "Earnings": [0], "Change %": [0], "Status": [trade_type.upper()]
    })
    df = pd.concat([df, new_trade], ignore_index=True)
    df.to_csv(USER_DATA_FILE, index=False)

    if trade_type == "buy":
        update_balance(-total_cost)  # Deduct balance
    elif trade_type == "sell":
        update_balance(total_cost)  # Add balance

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
