### 소스코드 받고 해야할 일

1. 가상환경 다운받기
   mac - `python3 -m venv venv`
   window - `py -m venv venv`, `python -m venv venv`
2. 가상환경 활성화
   mac - `source venv/bin/activate`
   window - `venv\Scripts\activate`
3. 가상환경에 라이브러리 깔기
   `pip install flask pymongo dnspython requests certifi`

templates 폴더에 자신의 html을 만들어 올려주세요
만약 파일을 분리하고싶다면 static파일을 만들어 올려주세요

### 깃 명령어

`git init`: 로컬 디렉토리를 깃 저장소로 초기화
`git clone 저장소url`: 리모트 저장소를 복제해서 로컬에 저장
`git add .`: 변경 사항을 전부 스테이징 영역으로 추가
`git commit -m "커밋메세지"`: 스테이징 영역에 추가한 변경 사항을 커밋
`git push`: 커밋한 내용을 리모트 저장소에 업로드
`git pull`: 리모트 저장소의 변경 사항을 로컬에 가져오기
