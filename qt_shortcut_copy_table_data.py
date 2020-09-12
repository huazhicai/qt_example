from PyQt5.QtWidgets import QApplication, QWidget, qApp
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *


class Ui_Form(object):  # UI类
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.tableView = QTableView(Form)
        self.tableView.setEnabled(True)
        self.tableView.setGeometry(5, 5, 400, 200)
        self.tableView.setObjectName("tableView")
        QMetaObject.connectSlotsByName(Form)


# 逻辑类
class StartRun(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)
        self.update_table_view()

    def update_table_view(self):
        data = [
            (1, '张三', 18),
            (2, '李四', 29),
            (3, '王五', 25),
            (4, '赵六', 26),
        ]
        columns = ['id', 'name', 'age']

        # 设置数据层次结构，rows cols
        model = QStandardItemModel(len(data), len(columns))
        model.setHorizontalHeaderLabels([str(i) for i in columns])
        for row in range(len(data)):
            for column in range(len(data[row])):
                item = QStandardItem(str(data[row][column]))
                model.setItem(row, column, item)  # 设置每个位置的文本值
        self.tableView.setModel(model)

    def keyPressEvent(self, event):  # 重写监听事件
        # 监听 CTRL+C 组合键，实现复制数据到黏贴板
        if (event.key() == Qt.Key_C) and QApplication.keyboardModifiers() == Qt.ControlModifier:
            text = selected_tb_text(self.tableView)
            if text:
                try:
                    clipboard = qApp.clipboard()
                    clipboard.setText(text)  # 复制到黏贴板
                except BaseException as e:
                    print(e)


# 复制选择表格数据
def selected_tb_text(table_view):
    try:
        indexes = table_view.selectedIndexes() 
        indexes_dict = {}
        for index in indexes:
            row, column = index.row(), index.column()
            if row in indexes_dict.keys():
                indexes_dict[row].append(column)
            else:
                indexes_dict[row] = [column]
        # 将数据表数据用制表符(\t)和换行符(\n)连接，使其可以复制到excel文件中
        text = ''
        for row, columns in indexes_dict.items():
            row_data = ''
            for column in columns:
                data = table_view.model().item(row, column).text()
                if row_data:
                    row_data = row_data + '\t' + data 
                else:
                    row_data = data 
            if text:
                text = text + '\n' + row_data
            else:
                text = row_data
        return text 
    except BaseException as e:
        print(e)
        return ''


if __name__ == '__main__':
    import sys 
    app = QApplication(sys.argv)
    instance = StartRun()
    sys.exit(app.exec_())