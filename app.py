import os
import threading
import webbrowser
import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ensure user_data directory exists
if not os.path.exists("user_data"):
    os.makedirs("user_data")

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/practice')
def practice():
    return render_template('practice.html')

@app.route('/simulator')
def simulator():
    return render_template('simulator.html')

@app.route('/stock', methods=['GET'])
def get_stock_data():
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        return jsonify({"error": "Missing ticker"}), 400

    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d", interval="5m")

    if hist.empty:
        return jsonify({"error": "Invalid ticker or no data available"}), 400

    # Filter market hours: 9:30 AM - 4:00 PM EST
    market_open = "09:30"
    market_close = "20:00"

    hist = hist.between_time(market_open, market_close)

    timestamps = hist.index.strftime('%H:%M').tolist()
    prices = hist['Close'].round(2).tolist()

    return jsonify({"timestamps": timestamps, "prices": prices})

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
