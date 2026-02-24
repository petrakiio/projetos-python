from flask import Flask

def open_server():
    app = Flask(__name__)
    app.run(host='localhost',debug=True,port=5000)

def request(ip):
    