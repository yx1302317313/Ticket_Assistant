from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProxyStyle
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QStyleOption
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QStyleOptionTab
from PyQt5.QtGui import QBrush, QTextOption, QPen
from PyQt5.QtCore import QRectF
from PyQt5 import QtCore
from PyQt5 import QtGui
import typing


class TabStyle(QProxyStyle):

    # override method
    def sizeFromContents(self, content_type: QStyle.ContentsType,
                         option: 'QStyleOption', size: QtCore.QSize, widget: QWidget):

        size = QProxyStyle.sizeFromContents(content_type, option, size, widget)

        if content_type == QStyle.CT_TabBarTab:
            size.transpose()
            size.setHeight(90)
            size.setWidth(44)

        return size

    def drawControl(self, element: QStyle.ControlElement, option: 'QStyleOption',
                    painter: QtGui.QPainter, widget: typing.Optional[QWidget] = ...):

        if element == QStyle.CE_TabBarTabLabel:
            tab = QStyleOptionTab(option)
            if tab:
                all_rect = tab.rect

                if tab.state and QStyle.State_Selected:
                    painter.save()
                    painter.setPen(QPen(0x89cfff))
                    painter.setBrush(QBrush(0x89cfff))
                    painter.drawRect(all_rect.adjusted(6, 6, -6, -6))
                    painter.restore()

                text_option = QTextOption()
                text_option.setAlignment(Qt.AlignCenter)
                if tab.state and QStyle.State_Selected:
                    painter.setPen(QPen(0xf8fcff))
                else:
                    painter.setPen(QPen(0x5d5d5d))
                painter.drawText(QRectF(all_rect), tab.text, text_option)
                return

        if element == QStyle.CE_TabBarTab:
            QProxyStyle.drawControl(element, option, painter, widget)


'''
    void drawControl(ControlElement element, const QStyleOption *option, 
    QPainter *painter, const QWidget *widget) const
    {
        if (element == CE_TabBarTabLabel) {
            if (const QStyleOptionTab *tab = qstyleoption_cast<const QStyleOptionTab *>(option)) {
                QRect allRect = tab->rect;

                if (tab->state & QStyle::State_Selected) {
                    painter->save();
                    painter->setPen(0x89cfff);
                    painter->setBrush(QBrush(0x89cfff));
                    painter->drawRect(allRect.adjusted(6, 6, -6, -6));
                    painter->restore();
                }
                QTextOption option;
                option.setAlignment(Qt::AlignCenter);
                if (tab->state & QStyle::State_Selected) {
                    painter->setPen(0xf8fcff);
                }
                else {
                    painter->setPen(0x5d5d5d);
                }

                painter->drawText(allRect, tab->text, option);
                return;
            }
        }

        if (element == CE_TabBarTab) {
            QProxyStyle::drawControl(element, option, painter, widget);
        }
    }
};
'''
