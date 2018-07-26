from flask import Flask


app = Flask(__name__)

@app.route('/', methods=['POST'])
def processing():
    return '6071d7c2'
