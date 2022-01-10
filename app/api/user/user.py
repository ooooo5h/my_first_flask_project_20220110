from pymysql import connect
from pymysql.cursors import DictCursor

# 사용자 정보에 관련된 기능들을 모아두는 모듈
# app.py에서 이 함수들을 끌어다 사용

def user_test():
    
    # 추가 기능 작성
    # DB에서 아이디,비밀번호를 조회해서 로그인 확인 등    
    
    return {
        'name' : '전은형',
        'bith_year' : 1991,        
    }
    
    
def login_test(id, pw):
    
    # id와 pw을 이용해서 SQL쿼리 작성 -> 결과에 따라 다른 응답 리턴
    db = connect(
        host='finalproject.cbqjwimiu76h.ap-northeast-2.rds.amazonaws.com',
        port=3306,
        user='admin',
        passwd='Vmfhwprxm!123',
        db='test_phone_book',
        charset = 'utf8',  
        cursorclass = DictCursor,
    )
    
    cursor = db.cursor()
    
    sql = f"SELECT * FROM users WHERE email='{id}'AND password='{pw}'"

    cursor.execute(sql)
    
    query_result = cursor.fetchone()   # 검색결과가 없으면 None이 리턴됨   / 검색결과가 있으면 그 사용자의 정보를 담은 dict가 리턴됨
    
    # 쿼리 결과가 None이면 아이디,비밀번호 맞는 사람이 없다 => 로그인 실패
    if query_result == None:
        return {
            'code' : 400,
            'message' : '아이디 또는 비밀번호가 잘못되었습니다.'
        }, 400
        
    # 검색결과가 있다 => 아이디와 비밀번호 모두 맞는 사람이 있다 => 로그인 성공
    else :
        return {
            'code' : 200,
            'message' : '로그인에 성공'
        }      
