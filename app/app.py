from flask import Flask, jsonify
from flask.templating import render_template

from .api import user_test

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
        return render_template('web_test.html')   # templates폴더 내부의 파일을 불러내는 역할
    
    
    @app.route("/json")
    def json_test():
        # JSON : 양식 => "이름표" : 실제 값의 조합(dictionary를 이용하면 작업이 편하다)
        test_dict = {}
        test_dict['name'] = '전은형'
        test_dict['birth_year'] = 1991
        test_dict['height'] = 165.6
        test_dict['is_male'] = False        
        
        return jsonify(test_dict)  # dict를 가지고 json으로 변경하는 함수를 활용해서 실제로 JSON 응답 내려주기
    
    
    @app.route("/json2")
    def json_test2():
        hello_dict = {}
        hello_dict['korean'] = '안녕하세요'
        hello_dict['english'] = 'Hello'
        
        return hello_dict
        
        
    @app.route("/json3")
    def json_test3():
        
        user_dict = {}
        user_dict['name'] = '전!은!형!'
        user_dict['birth_day'] = '1991-03-14'
        
        return {
            'code' : 200,
            'message' : '아니 이게 된다고?',
            'data' : user_dict           
        }
        
    @app.route('/module_test')
    def module_test():
        return user_test()
            
    # 이 서버를 사용하도록 결과로 내보내자
    return app