from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, DESCENDING
import uuid
from bson.objectid import ObjectId
import certifi
from datetime import datetime, timezone, timedelta

ca = certifi.where()
client = MongoClient(
    "mongodb+srv://mini:test@cluster0.dyeflfq.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=ca,
)
db = client.milk
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/jowon")
def jowon():
    return render_template("jowon.html")


@app.route("/changbum")
def changbum():
    return render_template("changbum.html")


@app.route("/minyoung")
def minyoung():
    return render_template("minyoung.html")


@app.route("/chaewon")
def chaewon():
    return render_template("chaewon.html")


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
    doc = {
        "id": id_receive,
        "name": name_receive,
        "img": img_receive,
        "comment": comment_receive,
    }
    db.team.insert_one(doc)
    return "", 204


@app.route("/member/update", methods=["PUT"])
def member_update():
    name_receive = request.get_json()["name"]
    img_receive = request.get_json()["img"]
    comment_receive = request.get_json()["comment"]
    member_id = request.get_json()["memberid"]

    result = db.team.update_one(
        {"id": member_id},
        {
            "$set": {
                "name": name_receive,
                "img": img_receive,
                "comment": comment_receive,
            }
        },
    )

    return "", 204


@app.route("/member/delete", methods=["DELETE"])
def member_del():
    member_id = request.args.get("memberid")
    db.team.delete_one({"id": member_id})
    return "", 204


# ======여기부터는 개인페이지 API입니다===========


@app.route("/members/<int:member_id>/comments", methods=["GET"])
def get_comments_with_id(member_id):
    if member_id != 2:
        comments = list(db.comments.find({"member_id": member_id}))
        for obj in comments:
            obj["_id"] = str(obj["_id"])

        return jsonify({"result": comments})

    elif member_id == 2:
        page = int(request.args.get("page"))
        limit = int(request.args.get("limit"))
        limit = limit if limit <= 20 else 20  # limit는 20 이상을 부여할 수 없습니다.

        count = db.comments.count_documents({"member_id": member_id})

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
            .sort("_id", DESCENDING)
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


@app.route("/members/<int:member_id>/comments", methods=["POST"])
def post_comments_with_id(member_id):
    data = {}
    data["member_id"] = member_id

    for key, value in request.form.items():
        if key == "member_id":  # formData에 들어간 member_id가 str로 담기므로 제외함
            continue
        data[key] = value

    kst = timezone(timedelta(hours=9))
    now = datetime.now(tz=kst)  # 한국 기준 현재시각을 출력합니다.
    data["upload_time"] = now
    db.comments.insert_one(data)

    return jsonify({"msg": "방명록 작성 완료!"})


@app.route("/members/<int:member_id>/comments/<comment_id>", methods=["DELETE"])
def delete_comments_with_id(member_id, comment_id):
    db.comments.delete_one({"_id": ObjectId(comment_id)})
    return jsonify({"msg": "방명록 삭제 완료!"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
