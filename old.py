import pymysql

import sys
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import uic, QtWidgets


form_class = uic.loadUiType("graph_test.ui")[0]

class graph(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.conn = pymysql.connect(host='localhost', user='root', password='qwer1234', db='test165', charset='utf8')
        self.cur = self.conn.cursor()
        self.cur.execute('SELECT * FROM old_man')
        self.read = self.cur.fetchall()
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.test_graph.addWidget(self.canvas)
        self.ax = self.fig.add_subplot(111)
        self.search_btn.clicked.connect(self.graph_search)


    def graph_search(self):
        self.ax.cla()
        print(self.first_year.currentText())
        print(self.read[0][2])
        year_list = []
        for i in range(int(self.first_year.currentText()),int(self.last_year.currentText())+1):
            year_list.append(i)
        print(year_list)
        first = self.read[0].index(float(self.first_year.currentText()))
        last = self.read[0].index(float(self.last_year.currentText()))
        print(first, last)
        print(year_list)
        for i in range(len(self.read)):
            if self.rate_test.currentText() in self.read[i][1]:
                print(i)
                self.ax.plot(year_list, self.read[i][first:last+1], 'r.-')
                print(self.read[0][2:])
                print(self.read[i][2:])
        self.canvas.draw()



    # def tableSet(self):
    #     self.testt.setRowCount(len(read))
    #     self.testt.setColumnCount(len(read[0]))
    #     self.testt.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #     for i in range(len(read)):
    #         for j in range(len(read[0])):
    #             self.testt.setItem(i, j, QTableWidgetItem(read[i][j]))
        # w = pg.PlotWidget(background='w')
        # self.setCentralWidget(w)
        #
        # x = np.arange(3)
        # years = ['2018', '2019', '2020']
        # values = [100, 400, 900]
        #
        # plt.bar(x, values)
        # plt.xticks(x, years)
        #
        # plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = graph()
    window.show()
    app.exec_()