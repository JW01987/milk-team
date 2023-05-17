from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import uuid
import certifi
from bson.objectid import ObjectId
ca = certifi.where()
client = MongoClient('mongodb+srv://mini:test@cluster0.dyeflfq.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.milk
app = Flask(__name__)

# 본인의 개인페이지를 아래 형식에 맞추어 넣어주세요
# 
# @app.route('/영문이름')
# def 함수이름():
#    return render_template('자신이 만든 html이름.html')

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/jowon')
def jowon():
   return render_template('jowon.html')
   
@app.route('/changbum')
def userhome():
   return render_template('personal_page.html')

#============여기부터는 메인 페이지 api 구현하는 곳입니다==========


#채원님 이거 참고하셔서 수정기능 만들면 쉬워요!!
#멤버 아이디(1=김창범,2=박민영,3=박채원,4=한조원)를 기준으로 검색 후 수정하시면 됩니다!
@app.route("/members", methods=["POST"])
def members():
    name_receive = request.get_json()['name']
    img_receive = request.get_json()['img']
    doc = {
        'name' :name_receive,
        'img' :img_receive
    }
    db.team.insert_one(doc)
    return '',204 #이건 성공/실패 코드입니다 api명세를 보면서 따라해주세요
    

@app.route("/memberlist", methods=["GET"])
def memberlist():
    memberlist = list(db.team.find({}, {'_id': 0}))
    return jsonify(memberlist)

# 채원님 이거 참고하셔서 만들면 금방 하실 수 있어요!!
# @app.route("/del", methods=["DELETE"])
# def movie_del():
#     allmovie = request.get_json()
#     reid = allmovie['id']
#     repw = allmovie['password']
#     db.movies.delete_one({'id':reid,'password':repw})
#     return jsonify(1)



#======여기부터는 개인페이지 API입니다===========


@app.route("/user/comment", methods=["POST"])
def guestbook_post():
    name_receive = request.form["name_give"]
    comment_receive = request.form["comment_give"]

    doc = {
        'master':'Changbum Kim',
        'name': name_receive,
        'comment': comment_receive
    }

    db.team.insert_one(doc)
    return jsonify({'msg':'방명록 작성 완료!'})

@app.route("/all_comment", methods=["GET"])
def guestbook_get():
    all_comments = list(db.team.find({'master':'Changbum Kim'},{'_id':False}))
    all_id = list(db.team.find({'master':'Changbum Kim'},{'_id':ObjectId()}))
    
    return jsonify({'result':all_comments,'resultid':obejectInCoder(all_id)})

def obejectInCoder(list):
    results=[]
    for document  in list:
        document ['_id'] = str(document ['_id'])
        results.append(document )
    return results

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)