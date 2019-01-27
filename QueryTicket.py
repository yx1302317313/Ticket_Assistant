from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate
from PyQt5.QtCore import pyqtSignal
from Crawler import *


class SingleTicket(QWidget):

    def __init__(self):
        super().__init__()

        self.src_label = QLabel("出发地")
        self.des_label = QLabel("目的地")
        self.date_label = QLabel("出发时间")

        self.src_text = QLineEdit()
        self.src_text.setClearButtonEnabled(True)
        self.src_text.setPlaceholderText("简称/全拼/汉字")
        self.src_text.setFixedWidth(200)

        self.des_text = QLineEdit()
        self.des_text.setClearButtonEnabled(True)
        self.des_text.setPlaceholderText("简称/全拼/汉字")
        self.des_text.setFixedWidth(200)

        # display selectable one month
        self.date_text = QDateEdit()
        self.date_text.setDateRange(QDate.currentDate(), QDate.currentDate().addMonths(1))
        self.date_text.setCalendarPopup(True)
        self.date_text.setFixedWidth(200)

        self.student_check = QCheckBox("学生")
        self.high_check = QCheckBox("高铁/动车")
        self.switch_button = QPushButton("←→切换")
        self.switch_button.setFixedWidth(100)
        self.query_button = QPushButton("查询")

        self.main_layout = QVBoxLayout()

        self.set_layout()
        self.connect_signal()

    def set_layout(self):

        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(self.src_label)
        h_layout1.addWidget(self.src_text)

        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(self.des_label)
        h_layout2.addWidget(self.des_text)

        h_layout3 = QHBoxLayout()
        h_layout3.addWidget(self.date_label)
        h_layout3.addWidget(self.date_text)

        h_layout4 = QHBoxLayout()
        h_layout4.addWidget(self.student_check)
        h_layout4.addWidget(self.high_check)
        h_layout4.addWidget(self.switch_button)

        self.main_layout.addLayout(h_layout1)
        self.main_layout.addLayout(h_layout2)
        self.main_layout.addLayout(h_layout3)
        self.main_layout.addLayout(h_layout4)
        self.main_layout.addWidget(self.query_button)
        self.main_layout.addSpacerItem(QSpacerItem(10, 100, QSizePolicy.Expanding, QSizePolicy.Fixed))

        self.setLayout(self.main_layout)

    def connect_signal(self):
        self.switch_button.clicked.connect(self.on_switch_button)
        self.query_button.clicked.connect(self.on_query_button)

    # signal
    query_signal = pyqtSignal(str, str, str, bool)

    # slots function
    def on_switch_button(self):

        temp_string = self.src_text.text()
        self.src_text.setText(self.des_text.text())
        self.des_text.setText(temp_string)

    def on_query_button(self):

        src = self.src_text.text()
        des = self.des_text.text()

        if src == '':
            QMessageBox.critical(self, "Error", "请输入出发地", QMessageBox.Ok)
            return
        if des == '':
            QMessageBox.critical(self, "Error", "请输入目的地", QMessageBox.Ok)
            return

        src = get_station_code(station_file, src)
        des = get_station_code(station_file, des)

        if src == "":
            QMessageBox.critical(self, "Error", "输入出发地有误", QMessageBox.Ok)
            return
        if des == "":
            QMessageBox.critical(self, "Error", "输入目的地有误", QMessageBox.Ok)
            return

        date = self.date_text.text()
        if self.student_check.isChecked():
            adult = False
        else:
            adult = True

        self.query_signal.emit(date, src, des, adult)


class DoubleTicket(SingleTicket):

    def __init__(self):
        self.return_date_label = QLabel("返程时间")

        self.return_date_text = QDateEdit()
        self.return_date_text.setDateRange(QDate.currentDate(), QDate.currentDate().addMonths(1))
        self.return_date_text.setCalendarPopup(True)
        self.return_date_text.setFixedWidth(200)

        super().__init__()

    def set_layout(self):
        super().set_layout()

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.return_date_label)
        h_layout.addWidget(self.return_date_text)

        self.main_layout.insertLayout(2, h_layout)

    def connect_signal(self):
        super().connect_signal()


class TransferTicket(SingleTicket):

    def __init__(self):
        super().__init__()

    def set_layout(self):
        super().set_layout()

    def connect_signal(self):
        super().connect_signal()


class QueryTicket(QWidget):

    def __init__(self):
        super().__init__()

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabShape(QTabWidget.Triangular)
        self.single = SingleTicket()
        self.double = DoubleTicket()
        self.transfer = TransferTicket()

        self.tab_widget.addTab(self.single, "单程")
        self.tab_widget.addTab(self.double, "往返")
        self.tab_widget.addTab(self.transfer, "连续换乘")
        self.set_layout()

    def connect_signal(self):
        pass

    def set_layout(self):
        main_layout = QHBoxLayout()
        main_layout.addSpacerItem(QSpacerItem(100, 10, QSizePolicy.Fixed, QSizePolicy.Expanding))
        main_layout.addWidget(self.tab_widget)
        main_layout.addSpacerItem(QSpacerItem(200, 10, QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.setLayout(main_layout)
