# import pymysql
# # list=['2000','20001']
# # num=int((list[0][2:]))
# # print(num)
# # word='2000'
# # a=int(word)
# # print(list[int(word[2:])+1])
# #
# # conn = pymysql.connect(host='127.0.0.1', user='root', password='chlwlgur', db='population',
# #                        charset='utf8')  # MY SQL 데이터 불러옴
# # c = conn.cursor()
# # c.execute("SELECT *FROM population.korea_birth")  # korea_birth table 조회
# # birth = c.fetchall()  # korea_birth table 리스트
# # print(birth
# #
# #
# #
# # conn = pymysql.connect(host='localhost', user='root', password='1234', db='jejudo',
# #                                charset='utf8')
# # cur = conn.cursor()
# # data = self.lineedit.text()
# # data2 = f"%{data}%"
# # sql = "SELECT * FROM jejudo.jeju_table WHERE full_address like %s"
# # cur.execute(sql, data2)
# # rows = cur.fetchall()
# #     for i in range(len(rows)):
# #         for j in range(len(rows[i])):
# #             self.table.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
# # conn.close()
# list=['2000년', '2001년', '2002년', '2003년', '2004년', '2005년', '2006년', '2007년', '2008년', '2009년', '2010년', '2011년', '2012년',
#                                      '2013년', '2014년', '2015년', '2016년', '2017년', '2018년', '2019년', '2020년', '2021년']
#
# empty=[]
# word='2000년'
# for i in list:
#     if word[2:4]<i[2:4]:
#         empty.append(i)
# print(empty)

import pymysql
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.rcParams['font.family'] ='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] =False
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


        #qt에 그래프 넣기
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.graph_verticalLayout.addWidget(self.canvas)
        self.ax = self.fig.add_subplot(111)




        conn = pymysql.connect(host='10.10.21.105', user='TT1', password='0000', db='population', charset='utf8') # MY SQL 데이터 불러옴
        c = conn.cursor()
        c.execute("SELECT *FROM population.test_table")# korea_birth table 조회

        self.birth = c.fetchall()
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
        del city_list[0:2] # 시군구별 항목 삭제

        # 시그널
        self.city_comboBox.addItems(city_list) # 콤보박스 아이템 추가
        self.city_comboBox.currentTextChanged.connect(self.first_year)
        self.year1_comboBox.currentTextChanged.connect(self.second_year)
        self.searching_btn.clicked.connect(self.searching)
        self.birth_Widget.cellChanged.connect(self.cellchange)# 셀값 변경 시그널


    def cellchange(self,row,col):
        # date2=self.birth_Widget.currentItem(row,col)
        data=self.birth_Widget.item(row,col) #변경된 셀값 data 변수 지정
        print("cell change", data.text())


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
        sql = "SELECT *FROM population.test_table WHERE 시군구별 = %s ";


        c.execute(sql, self.word1)
        info = c.fetchall()
        c.execute("SELECT *FROM population.test_table WHERE 시군구별 = '전국'")
        city_avg=c.fetchall()
        print(info)
        conn.commit()
        conn.close()

        searching_city=[]
        # searching_year=[]
        searching_rate=[]
        allcity_rate=[]
        col_list=['도시명']
        # row_list=[]


        # for j in self.birth[0]:
        #     if j != '시군구별':
        #         num=int(j)  # 스트링 인트형으로
        #         year_num=int(self.word2[0:4]) #스트링 --> 인트형
        #         # print(num)
        #         if year_num == num:
        #             searching_year.append(year_num)
        for i in self.birth:
            if self.word1 in i[0]:
                searching_city.append(self.word1)
        print(searching_city)


        for j in info:
            print(j)
            searching_rate.append(j[int(self.word2[2:4])+1:int(self.word3[2:4])+2]) # 비교 연도 사이 합계출산율
        for k in city_avg:
            allcity_rate.append(k[int(self.word2[2:4])+1:int(self.word3[2:4])+2]) # 비교연도 전국 합계출산율
        print('choi',allcity_rate)

        # for o in self.birth:
        #     if self.word1 in o[0]:
        #         row_list.append(o)
        #         row_list=set(row_list)
        # self.birth_Widget.setVerticalHeaderLabels(row_list)

        print(searching_city,searching_rate)
        # print(searching_rate[0][1])
        print(searching_rate[0])



        self.birth_Widget.setRowCount(2) # 행 개수
        self.birth_Widget.setColumnCount(len(searching_rate[0])+1) # 컬럼 개수
        self.birth_Widget.setItem(0,0, QTableWidgetItem(searching_city[0])) # 도시명
        self.birth_Widget.setItem(1,0, QTableWidgetItem("전국"))


        for l in range(int(self.word2[0:4]), int(self.word3[0:4]) + 1): # col name 들어갈 연도 범위
            col_list.append(str(l))
        print(col_list)
        self.birth_Widget.setHorizontalHeaderLabels(col_list) # col 항목명 세팅
        for m in range(1,len(searching_rate[0])+1):# 각 셀에 해당 연도 합계출산율 출력
            self.birth_Widget.setItem(0,m,QTableWidgetItem(str(searching_rate[0][m-1])))
            self.birth_Widget.setItem(1,m,QTableWidgetItem(str(allcity_rate[0][m-1])))

        rowcount=self.birth_Widget.rowCount()
        colcount=self.birth_Widget.columnCount()
        for s in range(0,rowcount):
            for t in range(0,colcount):
                data=self.birth_Widget.item(s,t)
                print(data.text())



        #그래프
        # plt.title(self.word1+' '+"출산율")
        # plt.plot(col_list[1:],searching_rate[0],label=self.word1) # 선택한 도시 그래프
        # plt.plot(col_list[1:],allcity_rate[0], label='전국') # 전국 도시 그래프
        # plt.legend()
        # plt.show()
        #

        # self.ax.cla() # 그래프 중첩되게 하지 않기위해서


        self.ax.cla()  # Clear the current figure

        x=col_list[1:]
        y=searching_rate[0]

        s=col_list[1:]
        t=allcity_rate[0]


        self.ax.plot(x, y, label=self.word1)
        self.ax.plot(s,t, label="전국")

        self.ax.set_title(self.word1+' '+"출산율")
        self.ax.legend()
        self.canvas.draw()













if __name__ == "__main__":
    app = QApplication(sys.argv)
    popup = Birth_Rate()
    popup.show()
    app.exec_()
