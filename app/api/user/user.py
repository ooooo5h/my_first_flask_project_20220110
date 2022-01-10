from pymysql import connect
from pymysql.cursors import DictCursor

# 사용자 정보에 관련된 기능들을 모아두는 모듈
# app.py에서 이 함수들을 끌어다 사용

# db연결 전담 변수
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


def user_test():
    
    # 추가 기능 작성
    # DB에서 아이디,비밀번호를 조회해서 로그인 확인 등    
    
    return {
        'name' : '전은형',
        'bith_year' : 1991,        
    }
    
    
def login_test(id, pw):
    
    ### 도전과제 : 이메일부터 있는지 검사하고, 해당 이메일이 없다면 "존재하지 않는 이메일입니다." message string으로 담아서 리턴하고 코드는 400으로
    # 이메일이 있다면? 추가 검사를 하자
    # 비밀번호도 맞는지 추가검사하고, 비밀번호가 맞다면 코드200으로 누가 로그인했는지 응답을 했는지(지금처럼 응답해주기)
    # => 비밀번호가 틀리다 => 이메일은 존재하는데, 비밀번호만 틀리단 이야기 => 비밀번호가 틀렸습니다 message string으로 리턴하고 코드 400
    sql = f"SELECT * FROM users WHERE email = '{id}'"
    
    cursor.execute(sql)
    email_check_result = cursor.fetchone()
    
    if email_check_result == None:
        return {
            'code' : 400,
            'message' : '존재하지 않는 이메일입니다.',
        }, 400
        
        
    sql = f"SELECT * FROM users WHERE password= '{pw}'"
        
    cursor.execute(sql)
    pw_check_result = cursor.fetchone()               
    if pw_check_result == None :
        return {
            'code' : 400,
            'message' : '비밀번호가 틀렸습니다.',
        }, 400
        
    else :
        return {
            'code' : 200,
            'message' : '000님 로그인에 성공하셨습니다.',
        },200
    
    
    
    
    # sql = f"SELECT * FROM users WHERE email='{id}'AND password='{pw}'"

    # cursor.execute(sql)
    
    # query_result = cursor.fetchone()   # 검색결과가 없으면 None이 리턴됨   / 검색결과가 있으면 그 사용자의 정보를 담은 dict가 리턴됨
    
    # # 쿼리 결과가 None이면 아이디,비밀번호 맞는 사람이 없다 => 로그인 실패
    # if query_result == None:
    #     return {
    #         'code' : 400,
    #         'message' : '아이디 또는 비밀번호가 잘못되었습니다.'
    #     }, 400
        
    # # 검색결과가 있다 => 아이디와 비밀번호 모두 맞는 사람이 있다 => 로그인 성공
    # else :
        
    #     # query_result가 실체가 있다(None이 아니다!!)  => 앱에서 사용 가능한 JSONObject로 보내보자
    #     print(query_result)
        
    #     user_dict = {
    #         'id' : query_result['id'],
    #         'email' : query_result['email'],
    #         'nickname' : query_result['nickname']
    #     }
        
    #     return {
    #         'code' : 200,
    #         'message' : '로그인에 성공',
    #         'data' : {
    #             'user' : user_dict,
    #         }
    #     }      


# 회원가입 함수
# 1. 이메일이 이미 사용중이라면 400으로 에러처리
# 2. 닉네임도 사용중이라면 400으로 에러처리
# 둘 다 통과해야 실제 INSERT INTO실행 후 200으로 결과 처리 + 가입된 사용자 정보도 내려주자
def sign_up(params):
    
    # 이메일이 사용중인지 먼저 확인
    # params['email']과 같은 이메일이 DB에 있는 지 조회해보자(SELECT문)
    
    sql = f"SELECT * FROM users WHERE email = '{params['email']}'"

    cursor.execute(sql)
    email_check_result = cursor.fetchone()   # 같은 이메일이 하나라도 있는가?
    
    if email_check_result :
        # 이메일 검사 쿼리의 결과가 None이 아니라 실체가 있다면
        # 이미 이메일이 사용중이라는 이야기 => DB에 등록 X
        return {
            'code' : 400,
            'message' : '이미 중복된 이메일입니다.',
        }, 400
        
    
    # 닉네임이 사용중인가? 사용중이라면 code-400, message - '이미 사용중인 닉네임입니다.'
    
    sql = f"SELECT * FROM users WHERE nickname = '{params['nick']}'"
    
    cursor.execute(sql)
    nickname_check_result = cursor.fetchone()
    
    if nickname_check_result:
        return {
            'code' : 400,
            'message' : '이미 사용중인 닉네임입니다.'
        }, 400
    
    
    sql = f"INSERT INTO users (email, password, nickname) VALUES ('{params['email']}','{params['pw']}','{params['nick']}'); "
    print(f'완성된 쿼리 : {sql}')
    
    cursor.execute(sql)
    db.commit()
    
    sign_up_user_sql = f"SELECT * FROM users ORDER BY id DESC LIMIT 1"
    cursor.execute(sign_up_user_sql)
    sign_up_user = cursor.fetchone()
    
    return {
        'code' : 200,
        'message' : '회원가입 성공',
        'data' : {
            'user' : {
                'id' : sign_up_user['id'],
                'email' : sign_up_user['email'],
                'nickname' : sign_up_user['nickname'],
            }
        }
    }