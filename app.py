from flask import Flask, render_template
import webbrowser
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def open_browser():
    webbrowser.get('open -a "Google Chrome" %s').open("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # Start a timer to open the browser after Flask starts
    threading.Timer(1.5, open_browser).start()  # Delay by 1.5 seconds
    app.run(debug=True)
