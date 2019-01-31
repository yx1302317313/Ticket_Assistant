from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import Crawler
import json


class TicketList(QWidget):

    def __init__(self):
        super().__init__()

        # init widget
        self.pre_button = QPushButton("前一天")
        self.pre_button.setFixedWidth(100)
        self.next_button = QPushButton("后一天")
        self.next_button.setFixedWidth(100)

        self.date_text = QDateEdit()
        self.date_text.setFixedWidth(200)
        self.date_text.setDateRange(QDate.currentDate(), QDate.currentDate().addMonths(1))
        self.date_text.setCalendarPopup(True)

        self.table = QTableWidget()
        self.table.setColumnCount(18)

        table_headers = ["车次",
                         "出发站",
                         "到达站",
                         "出发时间",
                         "到达时间",
                         "历时",
                         "特等座",
                         "一等座",
                         "二等座",
                         "高级软卧",
                         "软卧",
                         "动卧",
                         "硬卧",
                         "软座",
                         "硬座",
                         "无座",
                         "其他",
                         "备注"]

        self.table.setHorizontalHeaderLabels(table_headers)

        self.set_layout()
        self.connect_signal()

        # init info
        self.date = ""
        self.src = ""
        self.des = ""
        self.adult = True

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        if self.date_text.date() == QDate.currentDate():
            self.pre_button.setDisabled(True)

    def set_layout(self):

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.pre_button)
        h_layout.addWidget(self.date_text)
        h_layout.addWidget(self.next_button)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.table)

        self.setLayout(v_layout)

    def connect_signal(self):
        self.pre_button.clicked.connect(self.on_previous_button)
        self.next_button.clicked.connect(self.on_next_button)
        self.date_text.dateChanged.connect(self.on_date_changed)

    def set_date_text(self, date):
        self.date_text.setDate(date)

    def set_info(self, date, src, des, adult):
        self.date = date
        self.src = src
        self.des = des
        self.adult = adult

    # function
    def load_tickets(self, date: str, src: str, des: str, adult=True):
        # format the date
        date = Crawler.format_date(date)

        # get html from 12306
        html = Crawler.query_tickets(date, src, des, adult)

        try:
            # parser html and insert to ticket list
            html = dict(json.loads(html))
        except:
            # remove all row
            for i in range(0, self.table.rowCount()):
                self.table.removeRow(0)
            return

        # remove all row
        for i in range(0, self.table.rowCount()):
            self.table.removeRow(0)

        row = 0
        for i in html['data']['result']:
            # insert a row
            count = self.table.rowCount()
            self.table.insertRow(count)
            # get item data
            item = i.split('|')  # 用"|"进行分割
            # set item data
            self.table.setItem(row, 0, QTableWidgetItem(item[3]))  # 车次
            self.table.setItem(row, 1, QTableWidgetItem(Crawler.station_dict[item[6]]))  # 始发站
            self.table.setItem(row, 2, QTableWidgetItem(Crawler.station_dict[item[7]]))  # 终点站
            self.table.setItem(row, 3, QTableWidgetItem(item[8]))  # 出发时间
            self.table.setItem(row, 4, QTableWidgetItem(item[9]))  # 到达时间
            self.table.setItem(row, 5, QTableWidgetItem(item[10]))  # 历时
            self.table.setItem(row, 6, QTableWidgetItem(item[32] or item[25]))  # 商务座
            self.table.setItem(row, 7, QTableWidgetItem(item[31]))  # 一等座
            self.table.setItem(row, 8, QTableWidgetItem(item[30]))  # 二等座
            self.table.setItem(row, 9, QTableWidgetItem(item[21]))  # 高级软卧
            self.table.setItem(row, 10, QTableWidgetItem(item[23]))  # 软卧
            self.table.setItem(row, 11, QTableWidgetItem(item[27]))  # 动卧
            self.table.setItem(row, 12, QTableWidgetItem(item[28]))  # 硬卧
            self.table.setItem(row, 13, QTableWidgetItem(item[24]))  # 软座
            self.table.setItem(row, 14, QTableWidgetItem(item[29]))  # 硬座
            self.table.setItem(row, 15, QTableWidgetItem(item[26]))  # 无座
            self.table.setItem(row, 16, QTableWidgetItem(item[22]))  # 其他
            self.table.setItem(row, 17, QTableWidgetItem(item[1]))  # 备注

            row = row + 1

    # update list when date changed
    def update_table(self, date):
        self.load_tickets(date, self.src, self.des, self.adult)

    # slots function
    def on_previous_button(self):
        date = self.date_text.date().addDays(-1)
        self.date_text.setDate(date)

    def on_next_button(self):
        date = self.date_text.date().addDays(1)
        self.date_text.setDate(date)

    def on_date_changed(self, date):

        if date == QDate.currentDate():
            self.pre_button.setDisabled(True)
        elif date == QDate.currentDate().addMonths(1):
            self.next_button.setDisabled(True)
        else:
            self.pre_button.setEnabled(True)
            self.next_button.setEnabled(True)

        self.update_table(self.date_text.text())
