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
    
    # 연락처를 추가로 등록하는 sql 작성(어디에 넣을지 적는 란에는 DB(HeidiSQL)와 같은 명으로 작성)
    sql = f"INSERT INTO contacts (user_id, name, phone_num, memo) VALUES ({params['user_id']},'{params['name']}','{params['phone']}','{params['memo']}')"
    
    cursor.execute(sql)
    db.commit()
    
    return {
        'code' : 200,
        'message' : '연락처 등록 성공',
    }, 200
    
    
# 모든 연락처 조회
def get_contacts_from_db(params):
    # 기본버전 : 해당 사용자의 모든 연락처를 목록으로 만들어서 리턴
    # 응용버전1 : 파라미터의 최신순 or 이름순인지 정렬 순서를 입력받고 그에 맞게 리턴
    # 응용버전2 : 한번에 10개씩만 내려주자(게시판처럼, 페이징 처리)
    sql = f"SELECT * FROM contacts WHERE user_id = {params['user_id']}"
    
    cursor.execute(sql)
    query_result = cursor.fetchall()  # 목록을 가져와야하니까 fetchall
    
    # 클라이언트에게 전달해 줄 목록을 따로 변수로 추가(왜냐 리턴안에 주루루룩 하나하나 써주기 싫으니까)
    contacts_arr = []
    
    # DB의 실행결과 한 줄을 가지고, 여러가지 가공을 통해 클라이언트에게 전해줄 목록에 담기도록 돌린 반복문
    for row in query_result:
        
        # 클라이언트가 받아들이기 편리한 구조(딕셔너리)로 (가공된)연락처를 담아줌
        contact = {}
        
        # contact의 내용 채우자
        contact['id'] = row['id']
        contact['name'] = row['name']
        contact['phone_num'] = row['phone_num']
        contact['memo'] = row['memo']
        
        # datetime으로 오는 데이터를 str로 가공해서 담아보자
        # datetime -> str로 변경? ==> strftime 활용하면 됨 (2022-01-08 01:00:00 양식)
        contact['created_at'] = row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        # 내용이 채워진 contact를 리스트에 추가
        contacts_arr.append(contact)
    
    return{
        'code' : 200,
        'message' : '내 연락처 목록',
        'data' : {
            'contacts' : contacts_arr,    # 리스트를 통째로 응답으로 내보내줌 => JSONArray를 응답으로 주겠다는 뜻
        }
    }, 200