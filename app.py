from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
ca = certifi.where()
#client = MongoClient('',tlsCAFile=ca)몽고디비 url넣기
# db = client.컬렉션 이름넣기

client = MongoClient('mongodb+srv://mini:test@cluster0.dyeflfq.mongodb.net/?retryWrites=true&w=majority')
db = client.milk

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/user')
def userhome():
   return render_template('personal_page.html')

@app.route("/user/comment", methods=["POST"])
def guestbook_post():
    name_receive = request.form["name_give"]
    comment_receive = request.form["comment_give"]

    doc = {
        'master':'Changbum Kim',
        'name': name_receive,
        'comment': comment_receive
    }

    db.fan.insert_one(doc)
    return jsonify({'msg':'방명록 작성 완료!'})

@app.route("/all_comment", methods=["GET"])
def guestbook_get():
    all_comments = list(db.fan.find({'master':'Changbum Kim'},{'_id':False}))
    all_id = list(db.fan.find({'master':'Changbum Kim'},{'_id':ObjectId()}))
    
    return jsonify({'result':all_comments,'resultid':obejectInCoder(all_id)})

def obejectInCoder(list):
    results=[]
    for document  in list:
        document ['_id'] = str(document ['_id'])
        results.append(document )
    return results

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
