from flask import Flask
from flask.templating import render_template

def create_app():
    # 플라스크 서버를 변수에 담자
    app = Flask(__name__)
    
    # 서버에 대한 세팅 진행
    
    @app.route("/")     # 만들고있는 서버에 /(아무것도 안붙인주소)로 접속하면 보여줄 내용을 설정한 것
    def home():
        # return 내용 : HTML등 웹 프론트엔드 태그
        return "<h1>Hello World!!</h1>"   # Hello World문장 리턴 => 이 내용을 사용자에게 보여주겠다.
    
    
    @app.route("/test")   # 서버의 /test주소로 오면 수행해줄 일을 작성
    def test():
        return "여기는 테스트 페이지야"
    
    
    @app.route("/web")
    def web_test():
        return render_template('web_test.html')
    
    # 이 서버를 사용하도록 결과로 내보내자
    return app