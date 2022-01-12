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
    
    # 연락처를 추가하기전에, user_id가 실존하나 확인하기
    sql = f"SELECT * FROM users WHERE id = {params['user_id']}"
    
    cursor.execute(sql)
    user_id_result = cursor.fetchone()
    
    if user_id_result is None:
        return{
            'code' : 400,
            'message' : '존재하지않는 유저의 id입니다.'
        }, 400
    
    
    sql = f"INSERT INTO contacts (user_id, name, phone_num, memo) VALUES ({params['user_id']}, '{params['name']}', '{params['phone']}','{params['memo']}')"
    
    cursor.execute(sql)
    db.commit()
    
    return {
        'code' : 200,
        'message' : '연락처 등록 성공'
    }