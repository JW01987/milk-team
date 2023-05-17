from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, DESCENDING
from datetime import datetime
import certifi

ca = certifi.where()
# client = MongoClient('',tlsCAFile=ca)몽고디비 url넣기
# db = client.컬렉션 이름넣기
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

# 제 개인 페이지로 랜더링합니다.
# http://127.0.0.1:5001/members/2가 입력되면 pmy.html로 이동합니다.
@app.route("/minyoung")
def home():
    return render_template("minyoung.html")

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
    now = datetime.now() # 본인의 PC 기준 현재시각을 출력합니다.
    now = datetime.strftime(now, "%Y-%m-%d %H:%M:%S") # 현재시각의 형식을 (2022-5-17 14:30:32)의 형태로 변환합니다.


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
@app.route("members/2/comments", methods=["GET"])
def get_comments():
    """페이지네이션을 구현합니다.
      - 쿼리로 page와 limit에 대한 정보를 받습니다.
      - page는 페이지네이션에서 현재 페이지를 의미합니다.
      - limit는 한 페이지당 보여줄 코멘트 수를 의미합니다.
    """
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))
    limit = limit if limit <= 20 else 20 # limit는 20 이상을 부여할 수 없습니다.

    count = db.comments.count_documents({})

    # 페이지네이션 작동에 사용될 변수입니다.
    # 만약 현재 3페이지에 머물고 있다면 페이지네이션은 <1 2 3 4 5>까지만 보여집니다.
    # 만약 7페이지에 머물고 있다면 페이지네이션은 <6 7 8 9 10>까지만 보여집니다.
    page_set = 5 # 페이지네이션의 페이지 숫자를 5개 단위로 보여지도록 합니다.
    page_group_num = (page - 1) // page_set
    start_page = page_group_num * page_set + 1
    end_page = (page_group_num + 1) * page_set

    # MongoDB에서 코멘트 데이터 가져오기
    # skip과 limit 메소드를 사용하면 가져올 데이터의 범위를 설정할 수 있습니다.
    comments = list(
        db.comments.find({}, {"_id": False})
        .skip((page - 1) * limit)
        .limit(limit)
        .sort("upload_time", DESCENDING)
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
