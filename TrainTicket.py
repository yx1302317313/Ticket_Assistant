from PyQt5.QtWidgets import QStackedWidget
from QueryTicket import QueryTicket
from TicketList import TicketList
from PurchaseTicket import PurchaseTicket
from PyQt5.QtCore import pyqtSignal


class TrainTicket(QStackedWidget):

    def __init__(self):
        super().__init__()

        # init stack using list
        self.stack = []
        self.stack.append(0)

        self.query_ticket = QueryTicket()  # stack index 0
        self.ticket_list = TicketList()  # stack index 1
        self.purchase_ticket = PurchaseTicket()  # stack index 2

        # add widget to stack widget
        self.addWidget(self.query_ticket)
        self.addWidget(self.ticket_list)
        self.addWidget(self.purchase_ticket)

        self.set_layout()
        self.connect_signal()

    def connect_signal(self):
        self.query_ticket.single.query_signal.connect(self.on_query_signal)

    def set_layout(self):
        pass

    def push_stack(self, index):
        self.stack.append(index)

        if len(self.stack) > 1:
            self.disable_back_signal.emit(False)

    def pop_stack(self):
        # stack is not empty
        if len(self.stack):
            self.stack.pop()

    # signals
    disable_back_signal = pyqtSignal(int)

    # slots function
    def on_query_signal(self, date, src, des, adult):
        # change widget of train ticket
        self.setCurrentIndex(1)
        self.push_stack(1)

        # load tickets
        self.ticket_list.set_info(date, src, des, adult)
        self.ticket_list.load_tickets(date, src, des, adult)

    def on_back_action(self):
        if len(self.stack):
            self.stack.pop()
            index = self.stack[len(self.stack)-1]
            self.setCurrentIndex(index)

        if len(self.stack) <= 1:
            self.disable_back_signal.emit(True)
