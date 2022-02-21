from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return 'Goodbye World!'

app.run(host='0.0.0.0', port=80)
