from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
ca = certifi.where()
#client = MongoClient('',tlsCAFile=ca)몽고디비 url넣기
# db = client.컬렉션 이름넣기
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
