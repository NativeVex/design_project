import os
import sys

from flask import Flask

app = Flask(__name__)

@app.route('/test')
def test():
    print("Test!")
    return '<b>Test page</b>'
@app.route('/')
def index():
    print("Index!")
    return '<b>Index page</b>'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
