import pymysql
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic


# ui 클래스
form_class = uic.loadUiType("bir_rate.ui")[0]


class Birth_Rate(QWidget, form_class):  # 클래스 선언 Birth_Rate
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # qt에 그래프 넣기
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.graph_verticalLayout.addWidget(self.canvas)
        self.ax = self.fig.add_subplot(111)

        conn = pymysql.connect(host='10.10.21.105', user='TT1', password='0000', db='population',
                               charset='utf8')  # MY SQL 데이터 불러옴
        c = conn.cursor()
        c.execute("SELECT *FROM population.test_table")  # korea_birth table 조회

        self.birth = c.fetchall()
        for i in self.birth:
            print(i)

        conn.commit()
        conn.close()

        city_list = []  # city_list 선언
        for i in self.birth:
            city_list.append(i[0])  # city_list에 도시이름 추가
        del city_list[0:2]  # 시군구별 항목 삭제

        # 시그널
        self.city_comboBox.addItems(city_list)  # 콤보박스 아이템 추가
        self.city_comboBox.currentTextChanged.connect(self.first_year)
        self.year1_comboBox.currentTextChanged.connect(self.second_year)
        self.searching_btn.clicked.connect(self.searching)
        # self.birth_Widget.cellChanged.connect(self.cellchange)# 셀값 변경 시그널
        self.add_button.clicked.connect(self.add_data)
        self.modify_button.clicked.connect(self.modify_data)
        self.del_button.clicked.connect(self.del_data)

    def add_data(self):
        addcity_name = self.add_city.text()
        print(city_name)

        if addcity_name == '':  # add_city 라인에딧에 입력값 안쓰고 추가 눌렀을때 조건
            pass
        else:
            conn = pymysql.connect(host='10.10.21.105', user='TT1', password='0000', db='population',
                                   charset='utf8')  # MY SQL 데이터 불러옴
            c = conn.cursor()
            sql = f"INSERT INTO test_table (시군구별) VALUES ('{addcity_name}')"; # addcity_name 행추가
            c.execute(sql)
            conn.commit()
            conn.close()

    def modify_data(self):
        city_name = self.modify_city.text() # modify_city 라인에디트 텍스트
        year = self.modify_year.text() # modify_year 라인에디트 텍스트
        birth_rate = self.modify_birth.text() # modify_birth 라인 에디트 덱스트
        print(city_name)
        print(year)
        print(birth_rate)

        if city_name == '' or year == '' or birth_rate == '':
            pass
        else:
            conn = pymysql.connect(host='10.10.21.105', user='TT1', password='0000', db='population',
                                   charset='utf8')  # MY SQL 데이터 불러옴
            c = conn.cursor()
            sql = f"UPDATE test_table SET {year} = {birth_rate} WHERE 시군구별 = '{city_name}'"; # 각 라인에디트에 입력 받은 텍스트 항목을 조건으로 해서 수정 기능
            c.execute(sql)
            conn.commit()
            conn.close()

    def del_data(self):
        delcity_name = self.del_city.text()
        print(delcity_name)

        if delcity_name == '':  # add_city 라인에딧에 입력값 안쓰고 추가 눌렀을때 조건
            pass
        else:
            conn = pymysql.connect(host='10.10.21.105', user='TT1', password='0000', db='population',
                                   charset='utf8')  # MY SQL 데이터 불러옴
            c = conn.cursor()
            sql = f"DELETE FROM test_table WHERE 시군구별 = '{delcity_name}'"; # del_city line edit text 행값 삭제
            c.execute(sql)
            conn.commit()
            conn.close()


    def first_year(self):  # year1_comboBox items 추가
        if self.city_comboBox.currentText() == "도시선택":  # city 콥보박스에 도시선택이면 연도선택 안되게 하려고
            self.year1_comboBox.clear()
        else:
            self.year1_comboBox.addItems(
                ['2000년', '2001년', '2002년', '2003년', '2004년', '2005년', '2006년', '2007년', '2008년', '2009년', '2010년',
                 '2011년', '2012년',
                 '2013년', '2014년', '2015년', '2016년', '2017년', '2018년', '2019년', '2020년', '2021년'])

    def second_year(self):  # year2_comboBox item 추가
        if self.city_comboBox.currentText() == "도시선택": # city 콥보박스에 도시선택이면 연도선택 안되게 하려고
            self.year2_comboBox.clear()
        else:
            self.year2_comboBox.clear()  # 콤보박스 클리어
            add_year = []
            self.item_list = ['2000년', '2001년', '2002년', '2003년', '2004년', '2005년', '2006년', '2007년', '2008년', '2009년',
                              '2010년',
                              '2011년', '2012년', '2013년', '2014년', '2015년', '2016년', '2017년', '2018년', '2019년', '2020년',
                              '2021년']
            for i in self.item_list:
                if self.year1_comboBox.currentText()[2:4] < i[2:4]:  # year1_comboBox.currentText() 보다 큰 연도
                    add_year.append(i)
            self.year2_comboBox.addItems(add_year)  # year2_comboBoxd items 추가

    def searching(self):  # 검색 버튼 눌렀을때 메소드

        # 콤보박스 현재 텍스트 변수지정
        self.word1 = self.city_comboBox.currentText()
        self.word2 = self.year1_comboBox.currentText()
        self.word3 = self.year2_comboBox.currentText()

        conn = pymysql.connect(host='127.0.0.1', user='root', password='chlwlgur', db='population',
                               charset='utf8')  # MY SQL 데이터 불러옴
        c = conn.cursor()
        sql = "SELECT *FROM population.test_table WHERE 시군구별 = %s ";  # self.city_comboBox.currentText()를 조회하기 위해서
        c.execute(sql, self.word1)
        self.info = c.fetchall()
        c.execute(
            "SELECT *FROM population.test_table WHERE 시군구별 = '전국'")  # self.city_comboBox.currentText()가 전국인 테이터 조회
        city_avg = c.fetchall()
        print(self.info)
        conn.commit()
        conn.close()

        searching_city = []
        searching_rate = []
        allcity_rate = []
        self.col_list = ['도시명']

        for i in self.birth:
            if self.word1 in i[0]:
                searching_city.append(self.word1)

        for j in self.info:
            print(j)
            searching_rate.append(j[int(self.word2[2:4]) + 1:int(self.word3[2:4]) + 2])  # 비교 연도 사이 합계출산율
        for k in city_avg:
            allcity_rate.append(k[int(self.word2[2:4]) + 1:int(self.word3[2:4]) + 2])  # 비교연도 전국 합계출산율
        print('choi', allcity_rate)

        print(searching_city, searching_rate)
        print(searching_rate[0])

        self.birth_Widget.setRowCount(2)  # 행 개수
        self.birth_Widget.setColumnCount(len(searching_rate[0]) + 1)  # 컬럼 개수
        self.birth_Widget.setItem(0, 0, QTableWidgetItem(searching_city[0]))  # 도시명
        self.birth_Widget.setItem(1, 0, QTableWidgetItem("전국"))

        for l in range(int(self.word2[0:4]), int(self.word3[0:4]) + 1):  # col name 들어갈 연도 범위
            self.col_list.append(str(l) + '년')
        print(self.col_list)
        self.birth_Widget.setHorizontalHeaderLabels(self.col_list)  # col 항목명 세팅
        for m in range(1, len(searching_rate[0]) + 1):  # 각 셀에 해당 연도 합계출산율 출력
            self.birth_Widget.setItem(0, m, QTableWidgetItem(str(searching_rate[0][m - 1])))
            self.birth_Widget.setItem(1, m, QTableWidgetItem(str(allcity_rate[0][m - 1])))


        self.ax.cla()  # Clear the current figure

        x = self.col_list[1:]
        y = searching_rate[0]

        s = self.col_list[1:]
        t = allcity_rate[0]

        self.ax.plot(x, y, label=self.word1)
        self.ax.plot(s, t, label="전국")

        self.ax.set_title(self.word1 + ' ' + "출산율")
        self.ax.legend()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    popup = Birth_Rate()
    popup.show()
    app.exec_()