from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy


class Login(QDialog):

    def __init__(self):
        super().__init__()

        self.user_label = QLabel("用户名")
        self.password_label = QLabel("密 码")
        self.user_text = QLineEdit()
        self.user_text.setFixedWidth(200)
        self.password_text = QLineEdit()
        self.password_text.setFixedWidth(200)
        self.password_text.setEchoMode(QLineEdit.Password)  # set line edit as password mode
        self.cancel_button = QPushButton("取消")
        self.login_button = QPushButton("登录")

        self.init_widget()
        self.set_layout()
        self.connect_signal()

    # private method
    def init_widget(self):
        pass

    def set_layout(self):
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.user_label)
        user_layout.addWidget(self.user_text)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_text)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.login_button)

        center_layout = QVBoxLayout()
        center_layout.addSpacerItem(QSpacerItem(5, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))
        center_layout.addLayout(user_layout)
        center_layout.addSpacerItem(QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))
        center_layout.addLayout(password_layout)
        center_layout.addSpacerItem(QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))
        center_layout.addLayout(button_layout)
        center_layout.addSpacerItem(QSpacerItem(5, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))

        main_layout = QHBoxLayout()
        main_layout.addSpacerItem(QSpacerItem(30, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))
        main_layout.addLayout(center_layout)
        main_layout.addSpacerItem(QSpacerItem(30, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.setLayout(main_layout)
        self.setFixedSize(450, 300)

    def get_user(self):
        return self.user_text.text()

    def get_password(self):
        return self.password_text.text()

    def connect_signal(self):
        self.login_button.clicked.connect(self.on_login_button)
        self.cancel_button.clicked.connect(self.on_cancel_button)

    def on_cancel_button(self):
        self.done(0)

    def on_login_button(self):
        # user name and password are not empty
        if self.user_text.text() != "" and self.password_text.text() != "":
            self.done(1)
        else:
            QMessageBox.critical(self, "Error", "请输入用户名和密码", QMessageBox.Ok)
