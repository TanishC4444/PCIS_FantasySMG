import os
import threading
import webbrowser
import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)

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

    # Filter only market hours
    hist = hist.between_time("09:30", "16:00")

    timestamps = hist.index.strftime('%H:%M').tolist()
    prices = hist['Close'].round(2).tolist()

    # Fetch extra stock details
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

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
