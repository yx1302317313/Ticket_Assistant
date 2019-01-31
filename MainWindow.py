from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QAction
from UserInfo import UserInfo
from TrainTicket import TrainTicket
from TabStyle import TabStyle 
import Crawler 


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # init information
        self.setWindowIcon(QIcon("resource/train.png"))
        self.setWindowTitle("Ticket Assistant")
        self.resize(800, 600)

        # move to the center of screen
        self.move(int((QApplication.desktop().width() - self.width()) / 2),
                  int((QApplication.desktop().height() - self.height()) / 2))

        # init widget

        # tool bar
        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)
        self.back_action = QAction(QIcon("resource/back.png"), "后退", self)
        self.back_action.setDisabled(True)
        self.next_action = QAction(QIcon("resource/next.png"), "前进", self)
        self.close_action = QAction(QIcon("resource/close.png"), "关闭", self)
        self.renew_action = QAction(QIcon("resource/renew.png"), "刷新", self)

        self.tool_bar.addAction(self.back_action)
        self.tool_bar.addAction(self.next_action)
        self.tool_bar.addAction(self.close_action)
        self.tool_bar.addAction(self.renew_action)

        # tab widget
        self.table = QTabWidget()
        self.status_bar = QStatusBar()
        self.user_info = UserInfo()
        self.train_ticket = TrainTicket()

        self.table.setTabPosition(QTabWidget.West)
        self.table.tabBar().setStyle(TabStyle())
        # self.table.tabBar().setStyle(TabStyle())

        # add tab
        self.table.addTab(self.train_ticket, "火车票")
        self.table.addTab(self.user_info, "个人信息")

        self.set_layout()
        self.connect_signal()

        # load info 
        Crawler.load_train_code(Crawler.station_file, Crawler.station_dict,Crawler.code_dict)

    def connect_signal(self):
        self.table.currentChanged.connect(self.on_tab_changed)

        # connect defined signals
        self.train_ticket.disable_back_signal.connect(self.on_disable_back)

        # connect action with slots
        self.back_action.triggered.connect(self.train_ticket.on_back_action)
        self.next_action.triggered.connect(self.on_next_action)
        self.renew_action.triggered.connect(self.on_renew_action)
        self.close_action.triggered.connect(self.on_close_action)

    def set_layout(self):
        self.addToolBar(self.tool_bar)
        self.init_status_bar()
        self.setCentralWidget(self.table)

    def init_status_bar(self):
        label = QLabel("CopyRight©2019 YuanXu")

        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignCenter)
        self.status_bar.addPermanentWidget(label)  # add permanent label for status bar
        self.setStatusBar(self.status_bar)  # set status bar for main window

    # slots function
    def on_tab_changed(self, index):

        if index == 0:
            self.back_action.setEnabled(True)
            self.next_action.setEnabled(True)
            self.close_action.setEnabled(True)
            self.renew_action.setEnabled(True)
            if len(self.train_ticket.stack) <= 1:
                self.back_action.setDisabled(True)

        elif index == 1:
            self.back_action.setDisabled(True)
            self.next_action.setDisabled(True)
            self.close_action.setDisabled(True)
            self.renew_action.setDisabled(True)
            self.user_info.load_info()

    def on_disable_back(self, disable):
        if disable:
            self.back_action.setDisabled(True)
        else:
            self.back_action.setEnabled(True)

    def on_back_action(self):
        pass

    def on_next_action(self):
        pass

    def on_renew_action(self):
        pass

    def on_close_action(self):
        pass


def main():
    # set organization and application name for global parameter settings
    QApplication.setOrganizationName("YuanXu")
    QApplication.setApplicationName("TicketAssistant")

    app = QApplication([])

    main_window = MainWindow()
    main_window.show()

    return app.exec()


if __name__ == '__main__':
    main()
