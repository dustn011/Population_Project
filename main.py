import pymysql
import sys
import matplotlib.pyplot as plt
import copy
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.rcParams['font.family'] ='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] =False
from matplotlib import font_manager, rc

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import uic, QtWidgets



# ui 클래스
form_class = uic.loadUiType("population_main.ui")[0]


class Population_Db(QWidget, form_class): # 클래스 선언 Birth_Rate
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        #qt에 그래프 넣기
        self.pic = plt.Figure()
        self.picture = FigureCanvas(self.pic)
        self.graph_verticalLayout.addWidget(self.picture)
        self.ax = self.pic.add_subplot(111)




        conn = pymysql.connect(host='10.10.21.105', user='TT1', password='0000', db='population', charset='utf8') # MY SQL 데이터 불러옴
        c = conn.cursor()
        c.execute("SELECT *FROM population.korea_birth") # korea_birth 조회

        self.birth = c.fetchall()
        for i in self.birth:
            print(i)

        conn.commit()
        conn.close()


        self.city_list = [] #city_list 선언
        for i in self.birth:
            self.city_list.append(i[0]) # city_list에 도시이름 추가
        del self.city_list[0:2] # 시군구별 항목 삭제

        # 시그널
        self.city_comboBox.addItems(self.city_list) # 콤보박스 아이템 추가
        self.city_comboBox.currentTextChanged.connect(self.year_first)
        self.year1_comboBox.currentTextChanged.connect(self.second_year)
        self.searching_btn.clicked.connect(self.searching)
        self.add_button.clicked.connect(self.add_data)
        self.modify_button.clicked.connect(self.modify_data)
        self.del_button.clicked.connect(self.del_data)


##### ####### 연수
        # ---------- 그래프 캔버스 ----------

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        self.world_graph_verticalLayout.addWidget(self.canvas)

        # 한글 깨짐 오류 고치기
        font_path = "C:\\Windows\\Fonts\\gulim.ttc"  # 컴퓨터에 들어있는 폰트 경로 가져오기
        # font_manager는 import 해와야함
        font = font_manager.FontProperties(fname=font_path).get_name()
        # 이거는 잘 모르겠음 연구를 해봐야겠음
        rc('font', family=font)

        # 이거 어떻게 쓰는지 알아버렸음~ 설명하긴 귀찮고 링크 첨부함^^
        # http://daplus.net/python-matplotlib%EC%97%90%EC%84%9C-%EC%9D%B8%EC%88%98%EA%B0%80-fig-add_subplot-111%EC%9D%98-%EC%9D%98%EB%AF%B8%EB%8A%94-%EB%AC%B4%EC%97%87%EC%9E%85%EB%8B%88%EA%B9%8C/
        self.world_graph = self.fig.add_subplot(111)   ## 수정

        # ---------- ui 시그널 ----------

        # 1번째 국가 검색
        self.src_box1.returnPressed.connect(self.search1)
        self.btn_src1.clicked.connect(self.search1)
        # 2번째 국가 검색
        self.src_box2.returnPressed.connect(self.search2)
        self.btn_src2.clicked.connect(self.search2)

        # 콤보박스에 연도 넣어주기
        self.yyitem_list = ['2000년', '2001년', '2002년', '2003년', '2004년', '2005년', '2006년', '2007년', '2008년',
                            '2009년', '2010년', '2011년', '2012년', '2013년', '2014년', '2015년', '2016년', '2017년',
                            '2018년', '2019년', '2020년', '2021년']
        self.cmb_yy1.addItems(self.yyitem_list[:-1])
        self.cmb_yy2.addItems(self.yyitem_list[1:])

        # 첫 번째 콤보박스 설정해야 두 번째 콤보박스 설정 가능
        self.cmb_yy1.currentIndexChanged.connect(self.setyy1)

        # 초기화 버튼 누르면 다 지움
        self.btn_reset.clicked.connect(self.clrData)

        # 통계 버튼 누르면 통계 보여주게 함
        self.btn_stats.clicked.connect(self.checkBeforStats)

        # 그래프 만들기
        self.btn_graph.clicked.connect(self.checkBeforGraph)

        # 삭제 버튼 (누르면 선택 데이터 삭제)
        self.btn_worldDelete.clicked.connect(self.worldDelete)

        # 수정 버튼 (누르면 수정한 데이터들 모두 수정)
        self.btn_worldChange.clicked.connect(self.worldChage)

        # 추가 버튼 (누르면 라인에디트에 있는 텍스트 데이터에 추가)
        self.btn_worldAdd.clicked.connect(self.worldAdd)
        # self.led_worldAdd.returnPressed.connect(self.worldAdd)

######### 시혇############
        self.fig1 = plt.Figure()
        self.canvas1 = FigureCanvas(self.fig1)
        self.test_graph.addWidget(self.canvas1)
        self.gra = self.fig1.add_subplot(111)
        self.search_btn.clicked.connect(self.graph_search)
        self.graph_see.clicked.connect(self.graph_screen)
        self.chart_see.clicked.connect(self.chart_screen)
        self.add_btn.clicked.connect(self.add_motion)
        self.change_btn.clicked.connect(self.change_motion)
        self.del_btn.clicked.connect(self.del_motion)


############# 지혁 메소드#####################

    def add_data(self):
        addcity_name = self.add_city.text()
        print(addcity_name)

        if addcity_name == '':  # add_city 라인에딧에 입력값 안쓰고 추가 눌렀을때 조건
            pass
        else:
            conn = pymysql.connect(host='10.10.21.105', user='TT1', password='0000', db='population',
                                   charset='utf8')  # MY SQL 데이터 불러옴
            c = conn.cursor()
            sql = f"INSERT INTO korea_birth (시군구별) VALUES ('{addcity_name}')";
            c.execute(sql)
            conn.commit()
            conn.close()
            self.city_list.append(addcity_name) #추가한 도시명 self.city_list에 append
            self.city_comboBox.addItems(self.city_list)  # 콤보박스에 추가한 행 도시명 아이템 추가


    def modify_data(self):
        city_name=self.modify_city.text()
        year=self.modify_year.text()
        birth_rate=self.modify_birth.text()
        print(city_name)
        print(year)
        print(birth_rate)
        if city_name =='' or year =='' or birth_rate =='':
            pass
        else:
            conn = pymysql.connect(host='10.10.21.105', user='TT1', password='0000', db='population', charset='utf8') # MY SQL 데이터 불러옴
            c = conn.cursor()
            sql=f"UPDATE korea_birth SET {year} = {birth_rate} WHERE 시군구별 = '{city_name}'";
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
            sql = f"DELETE FROM korea_birth WHERE 시군구별 = '{delcity_name}'";
            c.execute(sql)
            conn.commit()
            conn.close()
        self.city_comboBox.clear() ## 클리어 안해주면 추가했던 도시명이 남아 있게 되서 클리어 해좀 ...
        self.city_list.remove(delcity_name)
        self.city_comboBox.addItems(self.city_list)  # 콤보박스에 삭제한 행 도시명 아이템에서 삭제


    def year_first(self): #year1_comboBox items 추가
        if self.city_comboBox.currentText()=="도시선택": #city 콥보박스에 도시선택이면 연도선택 안되게 하려고
            self.year1_comboBox.clear()
        else:
            self.year1_comboBox.addItems(['2000년', '2001년', '2002년', '2003년', '2004년', '2005년', '2006년', '2007년', '2008년', '2009년', '2010년', '2011년', '2012년',
                                     '2013년', '2014년', '2015년', '2016년', '2017년', '2018년', '2019년', '2020년', '2021년'])


    def second_year(self): #year2_comboBox item 추가
        if self.city_comboBox.currentText() == "도시선택":
            self.year2_comboBox.clear()
        else:
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

        conn = pymysql.connect(host='10.10.21.105', user='TT1', password='0000', db='population',
                               charset='utf8')  # MY SQL 데이터 불러옴
        c = conn.cursor()
        sql = "SELECT *FROM population.korea_birth WHERE 시군구별 = %s "; # self.city_comboBox.currentText()를 조회하기 위해서
        c.execute(sql, self.word1)
        self.info = c.fetchall()
        c.execute("SELECT *FROM population.korea_birth WHERE 시군구별 = '전국'") #self.city_comboBox.currentText()가 전국인 테이터 조회
        city_avg=c.fetchall()
        print(self.info)
        conn.commit()
        conn.close()

        searching_city=[]
        # searching_year=[]
        searching_rate=[]
        allcity_rate=[]
        self.col_list=['도시명']



        for i in self.city_list:
            print(i)
            if self.word1 in i:
                searching_city.append(self.word1)



        for j in self.info:
            print(j)
            searching_rate.append(j[int(self.word2[2:4])+1:int(self.word3[2:4])+2]) # 비교 연도 사이 합계출산율
        for k in city_avg:
            allcity_rate.append(k[int(self.word2[2:4])+1:int(self.word3[2:4])+2]) # 비교연도 전국 합계출산율
        print('choi',allcity_rate)


        print(searching_city,searching_rate)
        print(searching_rate[0])



        self.birth_Widget.setRowCount(2) # 행 개수
        self.birth_Widget.setColumnCount(len(searching_rate[0])+1) # 컬럼 개수
        self.birth_Widget.setItem(0,0, QTableWidgetItem(searching_city[0])) # 도시명
        self.birth_Widget.setItem(1,0, QTableWidgetItem("전국"))


        for l in range(int(self.word2[0:4]), int(self.word3[0:4]) + 1): # col name 들어갈 연도 범위
            self.col_list.append(str(l)+'년')
        print(self.col_list)
        self.birth_Widget.setHorizontalHeaderLabels(self.col_list) # col 항목명 세팅
        for m in range(1,len(searching_rate[0])+1):# 각 셀에 해당 연도 합계출산율 출력
            self.birth_Widget.setItem(0,m,QTableWidgetItem(str(searching_rate[0][m-1])))
            self.birth_Widget.setItem(1,m,QTableWidgetItem(str(allcity_rate[0][m-1])))






        self.ax.cla()  # Clear the current figure

        x=self.col_list[1:]
        y=searching_rate[0]

        s=self.col_list[1:]
        t=allcity_rate[0]


        self.ax.plot(x, y, label=self.word1)
        self.ax.plot(s,t, label="전국")

        self.ax.set_title(self.word1+' '+"출산율")
        self.ax.legend()
        self.picture.draw()

############# 연수 메소드 #################
    # 국가 추가하기 함수
    def worldAdd(self):
        # row추가할 국가명 저장
        add_country = self.led_worldAdd.text()

        # DB 연결하기
        conn = pymysql.connect(host='10.10.21.105', user='test', password='0000', db='population', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur = conn.cursor()

        # 국가명이 **인 row를 만들고 싶어
        sql = f"INSERT INTO popu_test (국가별) VALUES ('{add_country}')"

        # execute 메서드로 db에 sql 문장 전송
        cur.execute(sql)

        # commit을 수행하면 하나의 트렌젝션 과정을 종료하게 된다고 함
        conn.commit()
        # DB 닫아주기
        conn.close()

        # 라인에디트 지워줍니다~
        self.led_worldAdd.clear()
        # 데이터 잘 들어갔다고 확인 문구 출력
        QMessageBox.information(self, '추가 성공', '데이터를 입력하셨습니다')

    # 수정 버튼 누르면 실행되는 메서드
    def worldChage(self):
        # 선택 안했을 때 경고문구 출력하는 조건문
        if self.stats_tableWidget.currentColumn() == -1:
            QMessageBox.information(self, '선택 오류', '수정할 셀을 선택해주세요')
        else:
            # DB에 넣어줄 데이터 float형변환 시키기, 형변환 오류 뜨면 그냥 str 타입으로 두고 조건문으로 분기점 주기
            try:
                changeData_value = float(self.stats_tableWidget.currentItem().text())
            except ValueError:
                changeData_value = self.stats_tableWidget.currentItem().text()
            # float형 데이터 아닐때 경고문구 출력
            if type(changeData_value) != float:
                QMessageBox.information(self, '타입 오류', '숫자만 입력해주세요')
            # 국가명은 수정 불가능하게 조건문 달아줌
            elif self.stats_tableWidget.currentColumn() == 0:
                QMessageBox.information(self, '수정 불가', '국가명은 수정할 수 없습니다')
            # 수정 시작
            else:
                # print(self.stats)
                # print(self.stats_tableWidget.currentItem().text())
                # print(self.stats_tableWidget.currentRow())
                # print(self.stats_tableWidget.currentColumn())
                # print(self.stats[changeData_idx1][changeData_idx2])
                # print(column_name, country_name, changeData_value)

                # 선택한 셀의 row 인덱스 저장
                changeData_idx1 = self.stats_tableWidget.currentRow()
                # 선택한 셀의 column 인덱스 저장
                changeData_idx2 = self.stats_tableWidget.currentColumn()

                # 데이터의 칼럼명 -> 콤보박스 리스트로 찾기
                column_name = self.yyitem_list[changeData_idx2 - 1]
                # 데이터의 국가명 -> 검색한 리스트에서 찾기
                country_name = self.stats[changeData_idx1][0]

                # DB 연결하기
                conn = pymysql.connect(host='10.10.21.105', user='test', password='0000', db='population', charset='utf8')
                # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
                cur = conn.cursor()

                # 국가명은 **이고 컬럼은 ****연도인 값에 바꿀 값을 넣고 수정할래
                sql = f"UPDATE popu_test SET {column_name} = {changeData_value} WHERE 국가별 = '{country_name}'"

                # execute 메서드로 db에 sql 문장 전송
                cur.execute(sql)

                # commit을 수행하면 하나의 트렌젝션 과정을 종료하게 된다고 함
                conn.commit()
                # DB 닫아주기
                conn.close()

                # 바로 테이블 위젯에 적용시키게 메서드 실행
                self.dbtoCompare()
                self.statsTable()

    # 삭제 버튼 누르면 실행되는 메서드
    def worldDelete(self):
        # 테이블 위젯의 셀을 선택하지 않았을 때. 컬럼의 위치?는 -1로 나옴 currentItem으로 해도 됐었는데 누가 알려주셔서 함 해봣음
        if self.stats_tableWidget.currentColumn() == -1:
            QMessageBox.information(self, '선택 오류', '삭제할 셀을 선택해주세요')
        # 테이블 위젯에서 컬럼 이름이 나라인 셀을 지울려고 할 때(먼소리지?) 경고 문구 출력
        elif self.stats_tableWidget.currentColumn() == 0:
            QMessageBox.information(self, '삭제 불가', '국가명은 지울 수 없습니다')
        # 삭제 코드
        else:
            # print(self.stats)
            # print(self.stats_tableWidget.currentItem())
            # print(self.stats_tableWidget.currentRow(), '번째 로우')
            # print(self.stats_tableWidget.currentColumn(), '번째 컬럼')

            # 선택한 셀의 row 인덱스 저장
            deleteData_idx1 = self.stats_tableWidget.currentRow()
            # 선택한 셀의 column 인덱스 저장
            deleteData_idx2 = self.stats_tableWidget.currentColumn()

            # 데이터의 칼럼명 -> 콤보박스 리스트로 찾기
            column_name = self.yyitem_list[deleteData_idx2-1]
            # 데이터의 국가명 -> 검색한 리스트에서 찾기
            country_name = self.stats[deleteData_idx1][0]

            # # 둘이 똑같은 결과를 출력 어떤 방식이 더 좋을까?
            # print(self.stats_tableWidget.currentItem().text())
            # print(self.stats[deleteData_idx1][deleteData_idx2])

            # DB 연결하기
            conn = pymysql.connect(host='10.10.21.105', user='test', password='0000', db='population', charset='utf8')
            # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
            cur = conn.cursor()

            # 국가명은 **이고 컬럼은 ****연도인 값에 null을 넣고 삭제했다고 표시할래
            sql = f"UPDATE popu_test SET {column_name} = null WHERE 국가별 = '{country_name}'"

            # execute 메서드로 db에 sql 문장 전송
            cur.execute(sql)

            # commit을 수행하면 하나의 트렌젝션 과정을 종료하게 된다고 함
            conn.commit()
            # DB 닫아주기^^;;
            conn.close()

            # 바로 테이블 위젯에 적용시키게 메서드 실행
            self.dbtoCompare()
            self.statsTable()

    # 그래프 만들기 전 입력 확인 메서드
    def checkBeforGraph(self):
        # 스텍 위젯의 그래프 인덱스로 넘어감
        self.graph_stats.setCurrentIndex(0)
        # 첫 번째 비교 국가 입력 안했을 시
        if not self.country1.text():
            QMessageBox.information(self, '공백 오류', '비교할 첫 번째 국가를 입력해주세요')
        # 두 번째 비교 국가 입력 안했을 시
        elif not self.country2.text():
            QMessageBox.information(self, '공백 오류', '비교할 두 번째 국가를 입력해주세요')
        # 비교 연도 입력 안했을 시
        elif not self.cmb_yy2:
            QMessageBox.information(self, '연도 오류', '비교할 연도를 입력해주세요')
        # DB에서 통계 출력
        else:
            # DB 가져오기
            self.dbtoCompare()
            # 그래프 함수 실행
            self.graphWgt()

    # 그래프 위젯에 보여주기
    def graphWgt(self):
        # 이전에 만든 그래프 지우기
        self.world_graph.cla()

        # x축 데이터(콤보박스로 지정한 연도 범위)
        x_year = self.yyitem_list[self.idx1: self.idx2 + 1]

        # y축 데이터(국가1, 국가2 인구성장률 수치), 튜플값은 바꿀 수 없으니 리스트로 변환
        y1 = list(copy.deepcopy(self.stats[0]))
        y2 = list(copy.deepcopy(self.stats[1]))

        # 데이터 정제?
        for i in range(len(y1)):
            # 데이터값이 null이면
            if not y1[i]:
                # 그래프에선 0으로 나오게 함
                y1[i] = 0
            # y2 데이터도 여기서 한꺼번에 정제함^^
            if not y2[i]:
                y2[i] = 0

        # 국가 이름은 수치로 표현 못하니까 지움 그리고 그래프를 만들때 (x, y) 대응되는 갯수? 맞춰줘야함
        y1.pop(0)
        y2.pop(0)

        # y축의 범위 구하기 위해서 가장 작은 값 구하기
        if min(y1) < min(y2):
            y_min = min(y1)
        else:
            y_min = min(y2)

        # y축의 범위 구하기 위해서 가장 큰 값 구하기
        if max(y1) < max(y2):
            y_max = max(y2)
        else:
            y_max = max(y1)

        # 바탕에 격자 넣기 gird를 True로, y축 격자만 나오게 할려면 ", axis = 'y'" 추가해주면 됨
        self.world_graph.grid(True, axis = 'y')

        # 연도 범위 갯수만큼 x축 만들기
        self.world_graph.set_xticks([i for i in range(len(x_year))])
        # x축 이름 만들어주기(label정하기)
        self.world_graph.set_xticklabels(x_year)
        a = np.arange(len(x_year))
        # 막대그래프 만들기,
        self.world_graph.bar(a, y1, width=0.3, alpha=0.4, color='red', label=f'{self.stats[0][0]}')
        self.world_graph.bar(a+0.3, y2, width=0.3, alpha=0.4, color='green', label=f'{self.stats[1][0]}')

        # 범례 왼쪽 가운데에 표시
        self.world_graph.legend(loc=(0.01, 0.8))

        self.canvas.draw()

    # 입력한 값 초기화
    def clrData(self):
        self.country1.clear()
        self.country2.clear()
        self.cmb_yy2.clear()
        self.cmb_yy2.addItems(self.yyitem_list[1:])
        self.country_stackedWidget.setCurrentIndex(0)
        self.cmb_yy1.setCurrentIndex(0)
        self.list_country1.clear()
        self.list_country2.clear()
        self.stats_tableWidget.clear()
        self.world_graph.cla()

    # 통계 메서드 실행하기 전 입력 확인 메서드
    def checkBeforStats(self):
        # 스텍 위젯의 통계 인덱스로 넘어감
        self.graph_stats.setCurrentIndex(1)
        # 첫 번째 비교 국가 입력 안했을 시
        if not self.country1.text():
            QMessageBox.information(self, '공백 오류', '비교할 첫 번째 국가를 입력해주세요')
        # 두 번째 비교 국가 입력 안했을 시
        elif not self.country2.text():
            QMessageBox.information(self, '공백 오류', '비교할 두 번째 국가를 입력해주세요')
        # 비교 연도 입력 안했을 시
        elif not self.cmb_yy2:
            QMessageBox.information(self, '연도 오류', '비교할 연도를 입력해주세요')
        # DB에서 통계 출력
        else:
            # DB 가져오기
            self.dbtoCompare()
            # 통계 함수 실행
            self.statsTable()
            pass

    # DB 가져오기
    def dbtoCompare(self):
        # 선택한 첫 번째 비교 국가 문자열 저장
        self.cty1 = self.country1.text()
        # 선택한 두 번째 비교 국가 문자열 저장
        self.cty2 = self.country2.text()

        # 선택한 20nn년 ~ 20xx년 사이 범위 값 구하기
        self.idx1 = self.yyitem_list.index(self.cmb_yy1.currentText())
        self.idx2 = self.yyitem_list.index(self.cmb_yy2.currentText())

        # DB에서 select 할 문자열 만들기 ex) 2002년,2003년,2004년,2005년,2006년,2007년,2008년,2009년
        toaddtx = ''
        for txt in self.yyitem_list[self.idx1: self.idx2 + 1]:
            toaddtx += txt
            # 마지막 for문에서는 ', ' 안넣음
            if txt is self.yyitem_list[self.idx2]:
                pass
            else:
                toaddtx += ', '
        # print(toaddtx)  # 더 간단한 방법이 있을텐데 어떻게 해야할까...

        # sql DB와 연결
        src = pymysql.connect(host='10.10.21.105', user='test', password='0000', db='population', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur = src.cursor()

        # db로 전송할 문장 작성
        sqltxt = f'SELECT 국가별, {toaddtx} FROM popu_test where (국가별 = "{self.cty1}" or 국가별 = "{self.cty2}")'
        # excute 메서드로 db에 sql 문장 전송
        cur.execute(sqltxt)

        # 전체 나열 함수, 레코드를 배열(튜플) 형식으로 저장해준다(fetch : 나열하다 정렬하다)
        self.stats = cur.fetchall()
        src.close()

    # 통계 테이블에 보여주는 메서드
    def statsTable(self):
        headerLabels = []
        headerLabels += ['국가']
        headerLabels += self.yyitem_list[self.idx1 : self.idx2+1]

        # 컬럼 만들기
        self.stats_tableWidget.setColumnCount(len(headerLabels))
        self.stats_tableWidget.setHorizontalHeaderLabels(headerLabels)

        # 컬럼(header)을 너비에 맞추기
        self.stats_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 비교할 국가 데이터 넣을 row 만들기
        self.stats_tableWidget.setRowCount(2)

        # self.stats 사용하기
        for i in range(len(self.stats)):
            for j in range(len(self.stats[i])):
                # i번째 줄의 j번째 칸에 데이터를 넣어줌
                self.stats_tableWidget.setItem(i, j, QTableWidgetItem(str(self.stats[i][j])))

    # 첫 번째 콤보박스보다 두 번째 콤보박스가 더 높은숫자만 나오게 함
    def setyy1(self):
        # 연도 리스트에서 첫 번째 콤보박스가 선택한 연도의 인덱스 가져옴
        idx = self.yyitem_list.index(self.cmb_yy1.currentText())
        # 두 번째 콤보박스 요소 지우고 다시 써줌
        self.cmb_yy2.clear()
        # 첫 번째 콤보박스의 요소보다 더 인덱스 번호가 높은 요소만 넣음
        self.cmb_yy2.addItems(self.yyitem_list[idx+1:])

    # 1번째 국가 검색
    def search1(self):
        # 기존 검색 내역 삭제
        self.list_country1.clear()
        # 라인에디터에 검색한 텍스트 변수에 저장
        search_word = self.src_box1.text()

        # sql DB와 연결
        src = pymysql.connect(host='10.10.21.105', user='test', password='0000', db='population', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur = src.cursor()

        # excute 메서드로 db에 sql 문장 전송
        cur.execute(f"SELECT 국가별 FROM popu_test where 국가별 like '%{search_word}%'")
        # 전체 나열 함수, 레코드를 배열(튜플) 형식으로 저장해준다(fetch : 나열하다 정렬하다)
        searched = cur.fetchall()
        src.close()

        # 리스트 위젯의 행에 튜플 데이터 넣어줌
        for country in searched:
            # 리스트 위젯의 첫번째 줄부터 데이터를 넣어줌
            self.list_country1.addItem(country[0])

        self.list_country1.itemDoubleClicked.connect(self.prtCountry1)

    # 1번째 국가 검색 리스트 더블클릭 이벤트
    def prtCountry1(self):
        # 더블클릭한 국가 text 가져옴
        country = self.list_country1.currentItem().text()
        self.country1.setText(country)
        # 다음 2번째 국가 검색 위젯으로 넘어감
        self.country_stackedWidget.setCurrentIndex(1)
        # 검색 기록 삭제
        self.src_box1.clear()

    # 2번째 국가 검색
    def search2(self):
        # 기존 검색 내역 삭제
        self.list_country2.clear()
        # 라인에디터에 검색한 텍스트 변수에 저장
        search_word = self.src_box2.text()

        # sql DB와 연결
        src = pymysql.connect(host='10.10.21.105', user='test', password='0000', db='population', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur = src.cursor()

        # excute 메서드로 db에 sql 문장 전송
        cur.execute(f"SELECT 국가별 FROM popu_test where 국가별 like '%{search_word}%'")
        # 전체 나열 함수, 레코드를 배열(튜플) 형식으로 저장해준다(fetch : 나열하다 정렬하다)
        searched = cur.fetchall()

        src.close()

        # 리스트 위젯의 행에 데이터 넣어줌
        for country in searched:
            # 리스트 위젯의 첫번째 줄부터 데이터를 넣어줌
            self.list_country2.addItem(country[0])

        self.list_country2.itemDoubleClicked.connect(self.prtCountry2)

    # 2번째 국가 검색 리스트 더블클릭 이벤트
    def prtCountry2(self):
        # 더블클릭한 국가 text 가져옴
        country = self.list_country2.currentItem().text()

        # 같은 국가는 검색 못하게 함
        if bool(country == self.country1.text()):
            QMessageBox.information(self, '번복 오류', '이전에 선택한 국가와 똑같은 국가를 선택할 수 없습니다.')
        else:
            self.country2.setText(country)

    ########## 시형 메소드 ###################


    # 그래프화면으로 넘어감
    def graph_screen(self):
        self.chartorgraph.setCurrentIndex(0)
    # 표화면으로 넘어감
    def chart_screen(self):
        self.chartorgraph.setCurrentIndex(1)
    # 검색하면 실행
    def graph_search(self):
        self.region = self.rate_test.currentText()               # 지역에 해당하는 항복별로 그리기 위해
        conn = pymysql.connect(host='10.10.21.105', user='test', password='0000', db='population', charset='utf8')
        cur = conn.cursor()
        cur.execute('SELECT * FROM old_rate WHERE 행정구역별 like %s', self.region)
        read = cur.fetchall()
        cur.execute('SELECT * FROM young_rate WHERE 행정구역별 like %s', self.region)
        read_1 = cur.fetchall()
        cur.execute('SELECT * FROM total_rate WHERE 행정구역별 like %s', self.region)
        read_2 = cur.fetchall()                   # 항목별로 열기위해 하나씩 만들기
        conn.close()
        print(read, "노년부양비")
        print(read_1, "유소년부양비")
        print(read_2, "총부양비")
        if self.first_year.currentText() > self.last_year.currentText():
            QMessageBox.information(self, '에러', '연도를 순서대로 입력하세요')
        else:
            self.gra.cla()                                   # 그래프 그리기
            print(self.first_year.currentText())
            print(self.rate_test.currentText())
            year_list = []                                  # 그래프 연도를 문자열로 넣어야 소수점이 안보이는듯
            for i in range(2000, 2022):                     # 그래서 리스트에 하나씩 문자열로 넣음
                year_list.append(str(i))
            print(year_list,"rer")
            fir_year = year_list.index(self.first_year.currentText())   # x축에 사용할 연도의 범위 인덱스 찾기
            sec_year = year_list.index(self.last_year.currentText())
            print(fir_year, sec_year)
            self.gra.plot(year_list[fir_year:sec_year+1], read[0][fir_year+1:sec_year+2], 'r.-', label='노년부양비')
            self.gra.plot(year_list[fir_year:sec_year+1], read_1[0][fir_year+1:sec_year+2], 'b.-', label='유소년부양비')
            self.gra.plot(year_list[fir_year:sec_year+1], read_2[0][fir_year+1:sec_year+2], 'g.-', label='총부양비')
            self.gra.set_title(self.region)
            print("VJFHR")
            self.gra.legend(loc='upper left', fontsize=8)                    # 그래프에 넣기
            self.canvas1.draw()
            self.old_chart.setRowCount(3)
            self.old_chart.setColumnCount(len(read[0][fir_year:sec_year+1])+1)  # 컴럼 길이는 3가지 유형이 다 똑같아서 하나만 씀 콤보박스에서 첫번째로 선택한거부터 마지막 범위까지
            self.old_chart.setEditTriggers(QAbstractItemView.DoubleClicked)
            self.old_chart.setItem(0, 0, QTableWidgetItem(self.region))      # 0번은 지역명 넣기위해 따로 뺌
            self.old_chart.setItem(1, 0, QTableWidgetItem(self.region))
            self.old_chart.setItem(2, 0, QTableWidgetItem(self.region))
            for j in range(len(read[0][fir_year:sec_year+1])):
                self.old_chart.setItem(0, j+1, QTableWidgetItem(str(read[0][fir_year+1:sec_year+2][j])))
                self.old_chart.setItem(1, j+1, QTableWidgetItem(str(read_1[0][fir_year+1:sec_year+2][j])))
                self.old_chart.setItem(2, j+1, QTableWidgetItem(str(read_2[0][fir_year+1:sec_year+2][j])))
            self.insert_year = ['지역']                               # 칼럼에 지역이랑 연도 넣기
            self.insert_year += year_list[fir_year:sec_year + 1]
            self.old_chart.setColumnCount(len(self.insert_year))
            self.old_chart.setHorizontalHeaderLabels(self.insert_year)

    def add_motion(self):
        add_region = self.add_edit.text()                   # 추가할 지역 적기
        conn = pymysql.connect(host='10.10.21.105', user='test', password='0000', db='population', charset='utf8')
        cur = conn.cursor()
        cur.execute('INSERT INTO old_rate (행정구역별) VALUES (%s)', add_region)
        cur.execute('INSERT INTO young_rate (행정구역별) VALUES (%s)', add_region)
        cur.execute('INSERT INTO total_rate (행정구역별) VALUES (%s)', add_region)           # 지역 추가하면 연도별 데이터는 null값
        conn.commit()
        conn.close()
        self.rate_test.addItem(add_region)
        self.tableSet()


    def del_motion(self):
        selected_cell = self.old_chart.currentItem().text()     # 선택한 셀의 내용을 찾고
        selected_row = self.old_chart.currentRow()              # 로우도 구한다
        selected_col = self.old_chart.currentColumn()           # 컴럼도 역시 구한다
        selected_list = []
        for i in range(self.old_chart.columnCount()):           # 연도의 범위가 컬럼 길이인데 컬럼 수대로 만든다
            selected_list.append(self.old_chart.item(selected_row, i).text())   # 로우 전체를 넣는다
        if selected_cell != selected_list[0]:
            conn = pymysql.connect(host='10.10.21.105', user='test', password='0000', db='population', charset='utf8')
            cur = conn.cursor()
            if selected_row == 0:
                cur.execute(f'UPDATE old_rate SET {"`"+self.insert_year[selected_col]+"`"} = NULL WHERE 행정구역별 = "{selected_list[0]}"')
            elif selected_row == 1:
                cur.execute(f'UPDATE young_rate SET {"`"+self.insert_year[selected_col]+"`"} = NULL WHERE 행정구역별 = "{selected_list[0]}"')
            elif selected_row == 2:
                cur.execute(f'UPDATE total_rate SET {"`"+self.insert_year[selected_col]+"`"} = NULL WHERE 행정구역별 = "{selected_list[0]}"')
            conn.commit()
            conn.close()
            self.tableSet()
        else:
            QMessageBox.information(self, "에러", "데이터를 선택해주세요")

    def change_motion(self):
        selected_col = self.old_chart.currentColumn()
        if selected_col == -1:
            QMessageBox.information(self, "에러", "셀을 선택하세요")
        else:
            try:                                # 데이터 수정할 때 숫자만 입력 가능하게 만들기 위해 숫자일 때만 float형으로 변경
                change_cell = float(self.old_chart.currentItem().text())
            except ValueError:
                change_cell = self.old_chart.currentItem().text()
            print(change_cell)
            selected_row = self.old_chart.currentRow()
            selected_col = self.old_chart.currentColumn()
            selected_list = []
            for i in range(self.old_chart.columnCount()):           # 선택한 행의 모든 항복 넣기
                selected_list.append(self.old_chart.item(selected_row, i).text())
            if type(change_cell) != float:
                QMessageBox.information(self, "에러", "숫자를 입력하세요")
            elif change_cell != selected_list[0]:
                conn = pymysql.connect(host='10.10.21.105', user='test', password='0000', db='population', charset='utf8')
                cur = conn.cursor()
                if selected_row == 0:
                    cur.execute(
                        f'UPDATE old_rate SET {"`" + self.insert_year[selected_col] + "`"} = {change_cell} WHERE 행정구역별 = "{selected_list[0]}"')
                elif selected_row == 1:
                    cur.execute(
                        f'UPDATE young_rate SET {"`" + self.insert_year[selected_col] + "`"} = {change_cell} WHERE 행정구역별 = "{selected_list[0]}"')
                elif selected_row == 2:
                    cur.execute(
                        f'UPDATE total_rate SET {"`" + self.insert_year[selected_col] + "`"} = {change_cell} WHERE 행정구역별 = "{selected_list[0]}"')
                conn.commit()
                conn.close()
                self.tableSet()
            else:
                QMessageBox.information(self, "에러", "데이터를 선택해주세요")


    def tableSet(self):
        conn = pymysql.connect(host='10.10.21.105', user='test', password='0000', db='population', charset='utf8')
        cur = conn.cursor()
        cur.execute('SELECT * FROM old_rate WHERE 행정구역별 like %s', self.region)
        read = cur.fetchall()
        cur.execute('SELECT * FROM young_rate WHERE 행정구역별 like %s', self.region)
        read_1 = cur.fetchall()
        cur.execute('SELECT * FROM total_rate WHERE 행정구역별 like %s', self.region)
        read_2 = cur.fetchall()
        conn.close()
        year_list = []
        for i in range(2000, 2022):
            year_list.append(str(i))
        fir_year = year_list.index(self.first_year.currentText())  # x축에 사용할 연도의 범위 인덱스 찾기
        sec_year = year_list.index(self.last_year.currentText())
        self.old_chart.setRowCount(3)
        self.old_chart.setColumnCount(len(read[0][fir_year:sec_year + 1]) + 1)
        self.old_chart.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.old_chart.setItem(0, 0, QTableWidgetItem(self.region))
        self.old_chart.setItem(1, 0, QTableWidgetItem(self.region))
        self.old_chart.setItem(2, 0, QTableWidgetItem(self.region))
        for j in range(len(read[0][fir_year:sec_year + 1])):        # 연도 인덱스를 이용해 해당 연도에 맞는 데이터값 불러오기
            self.old_chart.setItem(0, j + 1, QTableWidgetItem(str(read[0][fir_year + 1:sec_year + 2][j])))      # 노년부양비부터 총부양비까지 차례대로 데이터 넣기
            self.old_chart.setItem(1, j + 1, QTableWidgetItem(str(read_1[0][fir_year + 1:sec_year + 2][j])))
            self.old_chart.setItem(2, j + 1, QTableWidgetItem(str(read_2[0][fir_year + 1:sec_year + 2][j])))
        self.insert_year = ['지역']
        self.insert_year += year_list[fir_year:sec_year + 1]
        self.old_chart.setColumnCount(len(self.insert_year))
        self.old_chart.setHorizontalHeaderLabels(self.insert_year)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    popup = Population_Db()
    popup.show()
    app.exec_()
