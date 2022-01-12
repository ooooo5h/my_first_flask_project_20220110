from pymysql import connect
from pymysql.cursors import DictCursor

from app.models import Contacts, contacts

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
    sql = f"INSERT INTO contacts (user_id, name, phone_num, memo, email) VALUES ({params['user_id']},'{params['name']}','{params['phone']}','{params['memo']}', '{params['email']}')"
    
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
    # ========> 이 파라미터는, (업데이트 하지 않았다면) 첨부되지 않을 수도 있다
    # 응용버전2 : 한번에 10개씩만 내려주자(게시판처럼, 페이징 처리)
    sql = f"SELECT * FROM contacts WHERE user_id = {params['user_id']}"
       
    # order_type파라미터가 실제로 올때만 추가 작업
    if 'order_type' in params.keys():
        order_type = params['order_type']
        if order_type == '최신순' :
            sql = f"{sql} ORDER BY created_at DESC"   # 기존 쿼리 뒤에, ORDER BY created_at DESC 추가
        elif order_type == '이름순' :
            sql = f"{sql} ORDER BY name"   # 기존 쿼리 뒤에, ORDER BY name 추가
        
        
    # 페이지의 번호가 들어오면, 그때 일정 갯수만큼 넘기고, 그 다음 n개를 가져오는 식으로 처리하자
    if 'page_num' in params.keys():
        page_num = int(params['page_num'])
        
        # 0페이지 : 0개 넘기고, 그 다음 2개
        # 1페이지 : 2개를 넘기고, 그 다음 2개
        # 2페이지 : 4개를 넘기고, 그 다음 2개 -> 넘기는 갯수 : page_num * 2 , 보여주는 갯수 : 2
        sql = f"{sql} LIMIT {page_num * 2}, 2"   
        
    print(sql)
       
    cursor.execute(sql)
    query_result = cursor.fetchall()  # 목록을 가져와야하니까 fetchall
    
    # 클라이언트에게 전달해 줄 목록을 따로 변수로 추가(왜냐 리턴안에 주루루룩 하나하나 써주기 싫으니까)
    contacts_arr = []
    
    # DB의 실행결과 한 줄을 가지고, 여러가지 가공을 통해 클라이언트에게 전해줄 목록에 담기도록 돌린 반복문
    for row in query_result:
        
        contact = Contacts(row)
        contacts_arr.append(contact.get_data_object())
    
    return{
        'code' : 200,
        'message' : '내 연락처 목록',
        'data' : {
            'contacts' : contacts_arr,    # 리스트를 통째로 응답으로 내보내줌 => JSONArray를 응답으로 주겠다는 뜻
        }
    }, 200
    
    
# 키워드를 가지고 검색하는 기능
# '경' => 조경진, 박진경 등등.. 경자가 포함되면 모두 리턴 + 본인이 가진 연락처 中
def search_contact(params):
    sql = f"SELECT * FROM contacts WHERE name LIKE '%{params['keyword']}%'"
    
    cursor.execute(sql)
    search_list = cursor.fetchall()
    
    contacts = []
    
    for row in search_list:
        contact = Contacts(row)   # DB에서 추출한 row를 표현하는 dictionary를 가지고, 모델 클래스인 Contacts 객체로 변환하는 작업
        contacts.append( contact.get_data_object())
    
    return {
        'code' : 200,
        'message' : 'search complete',
        'data' : {
            'contacts' : contacts,
        }
    }