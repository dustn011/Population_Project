import pymysql
import sys
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import uic, QtWidgets

#ㄴㅁㅇㅁㅈㄴㅁㅇㄴㅁㅇ
font_path = "C:\\Windows\\Fonts\\gulim.ttc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

form_class = uic.loadUiType("population_main.ui")[0]

class graph(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.test_graph.addWidget(self.canvas)
        self.gra = self.fig.add_subplot(111)
        self.search_btn.clicked.connect(self.graph_search)
        self.graph_see.clicked.connect(self.graph_screen)
        self.chart_see.clicked.connect(self.chart_screen)
        self.add_btn.clicked.connect(self.add_motion)
        self.change_btn.clicked.connect(self.change_motion)
        self.del_btn.clicked.connect(self.del_motion)

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
            self.canvas.draw()
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
    window = graph()
    window.show()
    app.exec_()