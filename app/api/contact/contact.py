from pymysql import connect
from pymysql.cursors import DictCursor

# 연락처와 관련된 모든 로직을 담당하는 파일
# DB연결 / cursor 변수
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


# 연락처 추가
def add_contact_to_db(params):
    
    # 연락처를 추가하기전에, user_id 파라미터의 값이 실제 사용자 id가 있나 확인하기
    sql = f"SELECT * FROM users WHERE id = {params['user_id']}"
    
    cursor.execute(sql)
    user_id_result = cursor.fetchone()
    
    if user_id_result is None:
        return {
            'code' : 400,
            'message' : '존재하지 않는 유저의 id입니다.'
        }, 400
    
    # print('받아오는 파라미터가 어떻게 되나요 : ', params)
    
    # 연락처를 추가로 등록하는 sql 작성(어디에 넣을지 적는 란에는 DB(HeidiSQL)와 같은 명으로 작성)
    sql = f"INSERT INTO contacts (user_id, name, phone_num, memo) VALUES ({params['user_id']},'{params['name']}','{params['phone']}','{params['memo']}')"
    print(sql)
    
    return {
        'code' : 200,
        'message' : '임시 연락처 추가 성공 응답',
    }