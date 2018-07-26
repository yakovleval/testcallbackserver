from flask import Flask


app = Flask(__name__)

@app.route('/', methods=['POST'])
def processing():
    return '6071d7c2'

if __name__ == '__main__':
    app.run()