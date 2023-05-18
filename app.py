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
    return jsonify(memberlist)

@app.route("/members", methods=["POST"])
def members():
    id_receive = str(uuid.uuid1())
    name_receive = request.get_json()["name"]
    img_receive = request.get_json()["img"]
    comment_receive = request.get_json()["comment"]
    doc = {"id":id_receive,"name": name_receive, "img": img_receive,"comment":comment_receive}
    db.team.insert_one(doc)
    return "", 204   

@app.route("/member/update", methods=["PUT"])
def member_update():
    member_id = request.get_json()["memberid"]
    name_receive = request.get_json()["name"]
    img_receive = request.get_json()["img"]
    comment_receive = request.get_json()["comment"]
    #result = db.team.update_one({"id":member_id},{"$set":{"name":name_receive,"img":img_receive,"comment":comment_receive}})
    result = db.team.update_one({"name":name_receive},{"$set":{"img":img_receive,"comment":comment_receive}})
    return "", 204


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


@app.route("/members/1/comments", methods=["GET"])
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
