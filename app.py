from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://mini:test@cluster0.dyeflfq.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.milk
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

# @app.route('/test',methods=["POST"])
# def test():
#    test = request.form['test']
#    db.fan.insert_one({"test":test})
#    return jsonify({'msg': '저장완료!'})

@app.route('/jowon')
def jowon():
   return render_template('jowon.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
