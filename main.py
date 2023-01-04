import pymysql
import sys
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic

# conn = pymysql.connect(host='127.0.0.1', user='root', password='chlwlgur', db='population', charset='utf8')
# c = conn.cursor()
# c.execute("SELECT *FROM population.korea_birth")
# birth = c.fetchall()
# for i in birth:
#     print(i)
# conn.commit()
# conn.close()

# ui 클래스
form_class = uic.loadUiType("bir_rate.ui")[0]


class Birth_Rate(QWidget, form_class): # 클래스 선언 Birth_Rate
    def __init__(self):
        super().__init__()
        self.setupUi(self)




        conn = pymysql.connect(host='127.0.0.1', user='root', password='chlwlgur', db='population', charset='utf8') # MY SQL 데이터 불러옴
        c = conn.cursor()
        c.execute("SELECT *FROM population.korea_birth")# korea_birth table 조회

        self.birth = c.fetchall() # korea_birth table 튜플 self.birth 변수에 대입
        for i in self.birth:
            print(i)
        # sql = "SELECT *FROM population.korea_birth WHERE 시군구별 = %s ";
        #
        # c.execute(sql,self.word1)
        # haha = print(c.fetchall())
        # data=f'{self.word2}'
        # sql = "SELECT %s FROM population.korea_birth";

        # c.execute(sql,data)
        # print(c.fetchall())
        conn.commit()
        conn.close()


        city_list = [] #city_list 선언
        for i in self.birth:
            city_list.append(i[0]) # city_list에 도시이름 추가
        del city_list[0] # 시군구별 항목 삭제
        # 시그널
        self.city_comboBox.addItems(city_list) # 콥보박스 아이템 추가
        self.city_comboBox.currentTextChanged.connect(self.first_year)
        self.year1_comboBox.currentTextChanged.connect(self.second_year)
        self.searching_btn.clicked.connect(self.searching)

    def first_year(self): #year1_comboBox items 추가
        self.year1_comboBox.addItems(['2000년', '2001년', '2002년', '2003년', '2004년', '2005년', '2006년', '2007년', '2008년', '2009년', '2010년', '2011년', '2012년',
                                     '2013년', '2014년', '2015년', '2016년', '2017년', '2018년', '2019년', '2020년', '2021년'])
    def second_year(self): #year2_comboBox item 추가
        self.year2_comboBox.clear() # 콤보박스 클리어
        add_year=[]
        self.item_list = ['2000년', '2001년', '2002년', '2003년', '2004년', '2005년', '2006년', '2007년', '2008년', '2009년', '2010년',
                '2011년', '2012년','2013년', '2014년', '2015년', '2016년', '2017년', '2018년', '2019년', '2020년', '2021년']
        for i in self.item_list:
            if self.year1_comboBox.currentText()[2:4]< i[2:4]: # year1_comboBox.currentText() 보다 큰 연도
                add_year.append(i)
        self.year2_comboBox.addItems(add_year)   # year2_comboBoxd items 추가


    def searching(self): # 검색 버튼 눌렀을때 메소드

        # 콤보박스 현재 텍스트 변수지정
        self.word1 = self.city_comboBox.currentText()
        self.word2 = self.year1_comboBox.currentText()
        self.word3 = self.year2_comboBox.currentText()

        conn = pymysql.connect(host='127.0.0.1', user='root', password='chlwlgur', db='population',
                               charset='utf8')  # MY SQL 데이터 불러옴
        c = conn.cursor()
        sql = "SELECT *FROM population.korea_birth WHERE 시군구별 = %s ";

        c.execute(sql, self.word1)
        info = c.fetchall()
        print(info)
        conn.commit()
        conn.close()

        searching_city=[]
        searching_year=[]
        searching_rate=[]
        col_list=['도시명']
        row_list=[]


        for j in self.birth[0]:
            if j != '시군구별':
                num=int(j)  # 스트링 인트형으로
                year_num=int(self.word2[0:4]) #스트링 --> 인트형
                # print(num)
                if year_num == num:
                    searching_year.append(year_num)
        for k in self.birth:
            if self.word1 in k[0]:
                searching_city.append(self.word1)
        # print(searching_city)


        for l in info:
            print(l)
            searching_rate.append(l[int(self.word2[2:4])+1:int(self.word3[2:4])+2]) # 비교 연도 사이 합계출산율

        # for o in self.birth:
        #     if self.word1 in o[0]:
        #         row_list.append(o)
        #         row_list=set(row_list)
        # self.birth_Widget.setVerticalHeaderLabels(row_list)

        print(searching_city,searching_year,searching_rate)
        # print(searching_rate[0][1])
        print(searching_rate[0])
        self.birth_Widget.setRowCount(1) # 행 개수
        self.birth_Widget.setColumnCount(len(searching_rate[0])+1) # 컬럼 개수
        self.birth_Widget.setItem(0,0, QTableWidgetItem(searching_city[0])) # 도시명

        for m in range(int(self.word2[0:4]), int(self.word3[0:4]) + 1): # col name 들어갈 연도 범위
            col_list.append(str(m))
        print(col_list)
        self.birth_Widget.setHorizontalHeaderLabels(col_list) # col 항목명 세팅
        for n in range(1,len(searching_rate[0])+1):
            self.birth_Widget.setItem(0,n,QTableWidgetItem(str(searching_rate[0][n-1])))

        plt.plot(col_list[1:],searching_rate[0])
        plt.show()


        #         self.word2=int(self.word2)
        #         if self.word2 == num:
        #             searching_year.append(self.word2)
        # print(searching_year)
        # #     if self.word2 in j:
        #         table_list.append(self.word2)










if __name__ == "__main__":
    app = QApplication(sys.argv)
    popup = Birth_Rate()
    popup.show()
    app.exec()
