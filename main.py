import pymysql
import sys
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


class Birth_Rate(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        conn = pymysql.connect(host='127.0.0.1', user='root', password='chlwlgur', db='population', charset='utf8')
        c = conn.cursor()
        c.execute("SELECT *FROM population.korea_birth")
        self.birth = c.fetchall()
        for i in self.birth:
            print(i)
        conn.commit()
        conn.close()


        city_list = []
        for i in self.birth:
            city_list.append(i[0])
        del city_list[0]
        # 시그널
        self.city_comboBox.addItems(city_list)
        self.city_comboBox.currentTextChanged.connect(self.year)
        self.searching_btn.clicked.connect(self.searching)

    def searching(self):
        table_list=[]
        self.word1=self.city_comboBox.currentText()
        self.word2=self.year_comboBox.currentText()
        for i in self.birth:
            if word1 in i[0]:
                print(i)



    def year(self):
        self.year_comboBox.addItems(['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012',
                                     '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021'])






if __name__ == "__main__":
    app = QApplication(sys.argv)
    popup = Birth_Rate()
    popup.show()
    app.exec()
