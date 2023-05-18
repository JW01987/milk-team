from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import uuid
import certifi
from bson.objectid import ObjectId
from datetime import datetime, timezone, timedelta

ca = certifi.where()
client = MongoClient(
    "mongodb+srv://mini:test@cluster0.dyeflfq.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=ca,
)
db = client.milk
app = Flask(__name__)

# 본인의 개인페이지를 아래 형식에 맞추어 넣어주세요
#
# @app.route('/영문이름')
# def 함수이름():
#    return render_template('자신이 만든 html이름.html')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/jowon")
def jowon():
    return render_template("jowon.html")


@app.route("/changbum")
def userhome():
    return render_template("personal_page.html")


@app.route("/minyoung")
def minyoung():
    return render_template("minyoung.html")


# ============여기부터는 메인 페이지 api 구현하는 곳입니다==========

@app.route("/memberlist", methods=["GET"])
def getmember():
    memberlist = list(db.team.find({}, {"_id": 0}))
    print(memberlist)
    return jsonify(memberlist)

# db.team.insert_one(데이터)는 데이터를 team 데이터베이스에 저장한다는 뜻입니다
# 채원님은 수정(업데이트)를 할거니까 update_one을 쓰시면 되겠죠?
# update_one(첫번째,{$set:{두번째}})은 두가지 내용을 받아요 첫번째는 어떤 걸 수정할건지의 "어떤 것"입니다 먼저 수정해야할 대상을 찾는거죠
# 멤버 아이디(1=김창범,2=박민영,3=박채원,4=한조원)를 기준으로 검색 후 수정하시면 됩니다!
# 멤버아이디로는 쿼리스트링(url에 낑겨서 온 데이터)을 사용할겁니다
# request.args.get('memberid') <- 쿼리 스트링에서(url) 멤버 아이디를 추출하는 방법
# 쿼리스트링에서 추출한 데이터를 첫번째에 넣어주면 되겠죠?
# $set은 그냥 약속입니다 수정할거면 이렇게 적어주세요~ 라 넘기셔도 되고 두번째를 채우면 됩니다 저장하기와 거의 똑같이 적어주시면 됩니다
#  name_receive = request.get_json()["name"] img_receive = request.get_json()["img"] 이름과 이미지를 가지고 오는 코드를 변수에 저장하고 딕셔너리 {} 애 넣어 코드를 적어주세요!
@app.route("/members", methods=["POST"])
def members():
    id_receive = str(uuid.uuid1())
    name_receive = request.get_json()["name"]
    img_receive = request.get_json()["img"]
    doc = {"id":id_receive,"name": name_receive, "img": img_receive}
    db.team.insert_one(doc)
    return "", 204   #이건 성공/실패 코드입니다 api명세를 보면서 따라해주세요

@app.route("/members/update", methods=["PUT"])
def member_update():
    member_id = request.args.get('memberid')
    name_receive = request.get_json()["name"]
    img_receive = request.get_json()["img"]
    db.team.insert_one({"id":member_id},{"$set":{{"name": name_receive, "img": img_receive}}})
    return "", 204


# db.movies.delete_one({'id':reid,'password':repw}) <-저희 데이터 베이스 이름은 team입니다 movies를 team으로 바꾸면 되겠죠?
# db.movies.delete_one({안에있는 걸 검색해서 삭제}) delete_one은 괄호안의 내용을 검색해 삭제한다는 뜻입니다 아래 코드는 아이디와 비밀번호를 이용해서 삭제했네요
# 저희는 쿼리스트링(url에 낑겨서 온 데이터)를 사용할겁니다
# request.args.get('memberid') <- 쿼리 스트링에서(url) 멤버 아이디를 추출하는 방법

# 아래는 예시 코드입니다 조금만 손보면 만들 수 있어요!
# @app.route("/del", methods=["DELETE"])
# def movie_del():
#     allmovie = request.get_json()
#     reid = allmovie['id']
#     repw = allmovie['password']
#     db.movies.delete_one({'id':reid,'password':repw})
#     return jsonify(1)

@app.route("/member/delete", methods=["DELETE"])
def member_del():
    member_id = request.args.get('memberid')
    db.team.delete_one({'id':member_id})
    return "", 204 




# ======여기부터는 개인페이지 API입니다===========


@app.route("/comments", methods=["POST"])
def guestbook_post():
    name_receive = request.form["name_give"]
    comment_receive = request.form["comment_give"]

    doc = {"member_id": 1,
            "nick_name": name_receive,
            "comment": comment_receive}

    db.comments.insert_one(doc)
    return jsonify({"msg": "방명록 작성 완료!"})


@app.route("/members/comments/1", methods=["GET"])
def guestbook_get():
    all_comments = list(db.comments.find({"member_id": 1}, {"_id": False}))
    all_id = list(db.comments.find({}, {"_id": ObjectId()}))
    return jsonify({"result": all_comments, "resultid": obejectInCoder(all_id)})


def obejectInCoder(list):
    results = []
    for document in list:
        document["_id"] = str(document["_id"])
        results.append(document)
    return results


# 개인 페이지 코멘트 POST API 입니다.
@app.route("/members/2/comments", methods=["POST"])
def post_comments():
    """코멘트 포스팅을 처리합니다.
    - 프론트에서 formData형식으로 닉네임과 패스워드, 코멘트정보를 전달받습니다.
    - 현재 시각과 맴버id를 추가하여 mongoDB에 추가합니다.
    """
    nickname = request.form["nickname"]
    password = request.form["password"]
    comment = request.form["comment"]

    # 현재시각을 변수로 지정합니다.
    # 저는 코멘트 POST요청을 받으면 현재시각을 생성하여 데이터베이스에 넣도록 했습니다.
    kst = timezone(timedelta(hours=9))
    now = datetime.now(tz=kst)  # 한국 기준 현재시각을 출력합니다.

    # 개인 페이지에 대한 댓글 정보
    post = {
        "member_id": 2,
        "nick_name": nickname,
        "comment": comment,
        "password": password,
        "upload_time": now,
    }

    # 데이터베이스에 저장합니다.
    db.comments.insert_one(post)

    return jsonify({"msg": "등록을 완료했습니다."})


# 개인 페이지 코멘트 GET API 입니다.
@app.route("/members/2/comments", methods=["GET"])
def get_comments():
    """페이지네이션을 구현합니다.
    - 쿼리로 page와 limit에 대한 정보를 받습니다.
    - page는 페이지네이션에서 현재 페이지를 의미합니다.
    - limit는 한 페이지당 보여줄 코멘트 수를 의미합니다.
    """
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))
    limit = limit if limit <= 20 else 20  # limit는 20 이상을 부여할 수 없습니다.

    count = db.comments.count_documents({})

    # 페이지네이션 작동에 사용될 변수입니다.
    # 만약 현재 3페이지에 머물고 있다면 페이지네이션은 <1 2 3 4 5>까지만 보여집니다.
    # 만약 7페이지에 머물고 있다면 페이지네이션은 <6 7 8 9 10>까지만 보여집니다.
    page_set = 5  # 페이지네이션의 페이지 숫자를 5개 단위로 보여지도록 합니다.
    page_group_num = (page - 1) // page_set
    start_page = page_group_num * page_set + 1
    end_page = (page_group_num + 1) * page_set

    # MongoDB에서 코멘트 데이터 가져오기
    # skip과 limit 메소드를 사용하면 가져올 데이터의 범위를 설정할 수 있습니다.
    comments = list(
        db.comments.find({"member_id": 2}, {"_id": False})
        .skip((page - 1) * limit)
        .limit(limit)
    )

    # 페이지네이션 구현에 필요한 정보를 프론트에 전달합니다.
    return jsonify(
        {
            "count": count,
            "start_page": start_page,
            "end_page": end_page,
            "page_set": page_set,
            "comments": comments,
        }
    )


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
