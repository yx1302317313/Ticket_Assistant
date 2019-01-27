from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings
from Login import Login


class UserInfo(QWidget):

    def __init__(self):
        super().__init__()

        # init widget
        self.name_label = QLabel("昵称")
        self.user_label = QLabel("用户名")
        self.email_label = QLabel("邮箱")
        self.sex_label = QLabel("性别")

        self.name_text = QLineEdit()
        self.name_text.setFixedWidth(300)
        self.user_text = QLineEdit()
        self.user_text.setFixedWidth(300)
        self.email_text = QLineEdit()
        self.email_text.setFixedWidth(300)

        self.secret_radio = QRadioButton("保密")
        self.secret_radio.setChecked(True)
        self.male_radio = QRadioButton("男")
        self.female_radio = QRadioButton("女")

        self.save_button = QPushButton("保存")
        self.save_button.setFixedWidth(100)
        self.exit_button = QPushButton("退出登录")
        self.exit_button.setFixedWidth(100)

        self.set_layout()
        self.load_info()
        self.connect_signal()

    def set_layout(self):

        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(self.name_label)
        h_layout1.addWidget(self.name_text)

        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(self.user_label)
        h_layout2.addWidget(self.user_text)

        h_layout3 = QHBoxLayout()
        h_layout3.addWidget(self.email_label)
        h_layout3.addWidget(self.email_text)

        h_layout4 = QHBoxLayout()
        h_layout4.addWidget(self.sex_label)
        h_layout4.addWidget(self.secret_radio)
        h_layout4.addWidget(self.male_radio)
        h_layout4.addWidget(self.female_radio)

        h_layout5 = QHBoxLayout()
        # h_layout5.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))
        h_layout5.addWidget(self.save_button)
        h_layout5.addWidget(self.exit_button)

        left_layout = QVBoxLayout()
        left_layout.addLayout(h_layout1)
        left_layout.addLayout(h_layout2)
        left_layout.addLayout(h_layout3)
        left_layout.addLayout(h_layout4)
        left_layout.addLayout(h_layout5)
        left_layout.addSpacerItem(QSpacerItem(10, 150, QSizePolicy.Expanding, QSizePolicy.Fixed))

        main_layout = QHBoxLayout()
        main_layout.addSpacerItem(QSpacerItem(100, 2, QSizePolicy.Fixed, QSizePolicy.Expanding))
        main_layout.addLayout(left_layout)
        main_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.setLayout(main_layout)

    def connect_signal(self):
        self.save_button.clicked.connect(self.on_save_button)
        self.exit_button.clicked.connect(self.on_exit_button)

    def clear_text(self):
        self.name_text.clear()
        self.user_text.clear()
        self.email_text.clear()
        self.secret_radio.setChecked(True)

    # load settings
    def load_info(self):

        settings = QSettings()
        login_info = settings.value("login", False, bool)

        # login
        if not login_info:
            login = Login()
            login_info = login.exec()    # 模式显示(会阻塞主线程)
            user = login.get_user()
            password = login.get_password()

            if login_info:
                self.save_user_info(user, password) # save user information who login in

        self.name_text.setText(settings.value("name", ""))
        self.user_text.setText(settings.value("user", ""))
        self.email_text.setText(settings.value("email", ""))

        # load sex of user
        sex = settings.value("user_sex", 1, int)
        if sex == 1:
            self.secret_radio.setChecked(True)
        elif sex == 2:
            self.male_radio.setChecked(True)
        elif sex == 3:
            self.female_radio.setChecked(True)

    # save application config information
    def save_info(self):
        settings = QSettings()
        settings.setValue("name", self.name_text.text())
        settings.setValue("user", self.user_text.text())
        settings.setValue("email", self.email_text.text())

        sex = 1
        if self.secret_radio.isChecked():
            sex = 1
        elif self.male_radio.isChecked():
            sex = 2
        elif self.female_radio.isChecked():
            sex = 3

        settings.setValue("user_sex", sex)

    def save_user_info(self, user, password):
        settings = QSettings()
        settings.setValue("login", True)
        settings.setValue("user", user)
        settings.setValue("password", password)

    def on_save_button(self):
        self.save_info()
        QMessageBox.information(self, "保存", "保存成功", QMessageBox.Ok)

    def on_exit_button(self):

        res = QMessageBox.question(self, "退出", "确认退出?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if res == QMessageBox.Yes:
            setting = QSettings()
            setting.clear()
            self.clear_text()
