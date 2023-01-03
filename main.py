# main code
import pymysql
conn=pymysql.connect(host='127.0.0.1', user='root', password='chlwlgur', db='population', charset='utf8')
c=conn.cursor()
birth=c.execute("SELECT *FROM population.korea_birth")
birth1=c.fetchall()
for i in birth1:
    print(i)