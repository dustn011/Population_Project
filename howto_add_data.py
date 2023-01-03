# DB의 테이블에 새로운 데이터 넣는 방법
import pymysql

# sql 데이터와 연결
conn = pymysql.connect(host='10.10.21.105', user= 'test', password='0000', db='population', charset='utf8')
# DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
cur = conn.cursor()

# db로 보내줄 문장 작성
grow_data = "SELECT * FROM popu_grow"
# excute 메서드로 db에 sql 문장 전송
cur.execute(grow_data)

# 전체 나열 함수, 레코드를 배열(튜플) 형식으로 저장해준다(fetch : 나열하다 정렬하다)
res = cur.fetchall()

# 23 번째 인덱스 : 대한민국 데이터
print(res[23], "평균:", '%0.2f'%((res[23][1] + res[23][2] + res[23][3])/3))
# 대한민국 근 3년간 평균 인구성장률 구하기 (0.07)
korea_avg = '%0.2f'%((res[23][1] + res[23][2] + res[23][3])/3)

asdf = 0
for data in res:
    if asdf == 0:
        asdf += 1
        pass
    else:
        # 국가별 근 3년간 평균 인구성장률 데이터
        country_avg = '%0.2f'%((data[1] + data[2] + data[3])/3)
        # 소수점 2자리까지만 표현하려고 '%0.2f'를 썼는데 이러면 데이터가 str형으로 저장됨 -> float 형으로 바꿔줌
        avg = float(country_avg)

        # 인구성장률 비교 데이터(위의 방식과 동일)
        compare = '%0.2f'%(float(korea_avg) - float(country_avg))
        com = float(compare)

        # sql 문법 만들어서 새로운 테이블에 value을 넣어줌
        sql = "INSERT INTO popu_compare (country, avg, compare) VALUES (%s, %s, %s)"
        # for문으로 한 줄 한 줄 넣어줍니다
        cur.execute(sql, (data[0], avg, com))

conn.commit()
conn.close()
