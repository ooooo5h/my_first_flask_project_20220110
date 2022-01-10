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
    # 아이디 : admin , 비밀번호 : qwer 이면 로그인 성공으로 응답
    # 그 외는 실패처리
    
    if id == 'admin' and pw == 'qwer':
        return {
            'code' : 200,
            'message' : 'login OK',
        } 
    else :
        return {
            'code' : 400,
            'message' : 'id or pw incorrect'
        }, 400