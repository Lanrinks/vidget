import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic, QtCore, QtTest
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QThread, QCoreApplication


import datetime
import time

H_show = [
    180, 181, 183, 185, 188,
    201, 222, 256, 311, 412,
    500, 520, ]

H_hide = [
    180,
    249, 338, 393, 427, 448,
    461, 469, 474, 477, 479,
    508, ]


def premier():
    import random
    from datetime import datetime, timedelta
    current_datetime = datetime.now()
    data_n = current_datetime.date()
    month_n = str(data_n)[:-2]
    data_now = data_n
    alfa = pd.read_csv('D:\\projects\\widget\\movies.csv', delimiter=';',
                       names=['name', 'year', 'rez', 'actor', 'data'])

    def finda(chislo):
        text = alfa[alfa['data'] == str(chislo)].index
        if len(text) > 0:
            return text[0]
        else:
            chislo = chislo + timedelta(days=1)
            return finda(chislo)

    j = finda(data_n)
    spisok = []
    if j + 4 <= len(alfa):
        for k in range(j, j + 5):
            add = {'num': 0, 'title': ''.join((alfa[k:k + 1]['name']).tolist()),
                   'year': ''.join((alfa[k:k + 1]['year']).tolist()),
                   'genres': ''.join((alfa[k:k + 1]['actor']).tolist()),
                   'data': ''.join((alfa[k:k + 1]['data']).tolist())}
            spisok.append(add)
    else:
        for k in range(j, len(alfa)):
            add = {'num': 0, 'title': ''.join((alfa[k:k + 1]['name']).tolist()),
                   'year': ''.join((alfa[k:k + 1]['year']).tolist()),
                   'genres': ''.join((alfa[k:k + 1]['actor']).tolist()),
                   'data': ''.join((alfa[k:k + 1]['data']).tolist())}
            spisok.append(add)

    spisok_r = []
    for x in range(31):
        ind_r = alfa[alfa['data'] == str(month_n)+str(x)].index
        if len(ind_r) > 0:
            for item in ind_r:
                spisok_r.append(item)
    j2 = int(random.choice(spisok_r))
    spisok2 = [
        {'num': 0, 'title': ''.join((alfa[j2 + 4:j2 + 5]['name']).tolist()),
         'year': ''.join((alfa[j2 + 4:j2 + 5]['year']).tolist()),
         'genres': ''.join((alfa[j2 + 4:j2 + 5]['actor']).tolist()),
         'data': ''.join((alfa[j2 + 4:j2 + 5]['data']).tolist())},
    ]

    return spisok, data_now, spisok2


class App(QWidget):
    show_more = True

    def __init__(self, app):
        QWidget.__init__(self)
        self.app = app
        self.set()
        self.setMore()

    def set(self):
        self.w_root = uic.loadUi('wid.ui')
        self.w_root.installEventFilter(self)
        self.w_root.btn_main.clicked.connect(self.setHeight)
        self.w_root.btn_random.clicked.connect(self.setRand)
        px_logo = QPixmap(f"img/kinopoisk.png")
        self.w_root.logo.setPixmap(px_logo)
        self.w_root.setWindowTitle('Кинопремьеры в России')
        self.w_root.setWindowIcon(QIcon(f"img/logo.png"))
        self.w_root.show()

    def eventFilter(self, object, event):
        self.w_root.resize(300, self.w_root.height())
        self.w_root.btn_main.move(0, self.w_root.height()-26)
        self.w_root.l_dayofweek.move(8, self.w_root.height() - 30)
        self.w_root.l_time.move(280, self.w_root.height() - 30)
        self.app.processEvents()
        return False

    def setHeight(self):
        if self.w_root.height() >= 508:
            self.show_more = False
        if self.show_more:
            for i in H_hide:
                if self.w_root.height() > i:
                    continue
                self.w_root.resize(400, i)
                self.w_root.btn_main.move(0, i-26)
                self.w_root.l_dayofweek.move(8, i-30)
                self.w_root.l_time.move(226, i-30)
                self.app.processEvents()
                time.sleep(0.02)
            self.show_more = False
        else:
            for i in reversed(H_show):
                self.w_root.resize(400, i)
                self.w_root.btn_main.move(0, i-26)
                self.w_root.l_dayofweek.move(8, i-30)
                self.w_root.l_time.move(226, i-30)
                self.app.processEvents()
                time.sleep(0.02)
            self.show_more = True
        app.show_more = self.show_more

    def setMore(self):
        cool, datanow, random_movie = premier()
        for i in cool:
            w_movie = uic.loadUi('movie.ui')
            w_movie.setObjectName('w'+str(i['num']))
            w_movie.label_name.setText(i['title'])
            w_movie.label_2.setText(i['year'])
            w_movie.label_3.setText(i['genres'])
            w_movie.label_4.setText(i['data'])
            self.w_root.box.addWidget(w_movie)
        self.w_root.l_data.setText(str(datanow))
        self.w_root.box.addStretch()

    def setRand(self):
        cool, datanow, random_movie = premier()
        for i in random_movie:
            self.w_root.label_name.setText(i['title'])
            self.w_root.label_2.setText(i['year'])
            self.w_root.label_3.setText(i['genres'])
            self.w_root.label_4.setText(i['data'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(app)
    app.exec_()
