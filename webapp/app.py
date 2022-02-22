import os
import sys

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Good evening'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
