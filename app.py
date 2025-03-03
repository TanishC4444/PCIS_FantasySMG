from flask import Flask, render_template
import webbrowser
import os

# Command Line: auto-py-to-exe
# Path: /Users/tanishchauhan/Desktop/PCIS_FantasySMG/app.py
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Automatically open the URL in Google Chrome on macOS
    webbrowser.get('open -a "Google Chrome" %s').open("http://127.0.0.1:5000/")
    app.run(debug=True)
