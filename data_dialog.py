import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *


# from graph.node_def.data_type import Bool, Int, Float, Str, List, Dict, Any, Event


class ArgsInputDialog(QDialog):
    def __init__(self, title, data_type, old_value, doneChangeCallback, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.data_type = data_type
        self.old_value = old_value
        self.doneChangeCallback = doneChangeCallback

        # self.data_display = QTextBrowser()
        self.data_display = QTextEdit()
        self.newInput = DataInputView.get_instance(title, data_type, self.data_display, self)

        # spliter = QSplitterHandle()

        originLabel = QLabel('原值: ')
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(originLabel.sizePolicy().hasHeightForWidth())
        originLabel.setSizePolicy(sizePolicy)

        originInput = QLabel(str(old_value))
        originInput.setMargin(5)
        originInput.setStyleSheet("background-color: rgb(193, 193, 193);")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(originInput.sizePolicy().hasHeightForWidth())
        originInput.setSizePolicy(sizePolicy)
        origin_layout = QHBoxLayout()
        origin_layout.addWidget(originLabel)
        origin_layout.addWidget(originInput)

        delButton = QPushButton('删除值')
        delButton.clicked.connect(self.delClicked)
        cancelButton = QPushButton('取消')
        cancelButton.clicked.connect(self.cancelClicked)
        saveButton = QPushButton('保存')
        saveButton.clicked.connect(self.saveClicked)
        saveButton.setDefault(True)

        layout = QGridLayout()
        layout.addWidget(self.newInput, 0, 0, 4, 3)
        layout.addWidget(self.data_display, 0, 3, 4, 3)
        layout.addLayout(origin_layout, 4, 0, 1, 3)
        layout.addWidget(delButton, 4, 3, 1, 1)
        layout.addWidget(cancelButton, 4, 4, 1, 1)
        layout.addWidget(saveButton, 4, 5, 1, 1)

        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

    def delClicked(self):
        self.doneChangeCallback(None, mode='del')
        super().accept()

    def cancelClicked(self):
        super().reject()

    def saveClicked(self):
        sig, value = self.parseValue()
        if not sig:
            QMessageBox.warning(None, 'Error', '输入值解析错误', QMessageBox.Ok)
            super().reject()
            return
        self.doneChangeCallback(value, mode='set')
        super().accept()

    def parseValue(self):
        try:
            text = str(self.newDisplay.toPlainText())
            print('user input', text)
        except:
            text = str(self.newDisplay.toPlainText())
        print(text)
        return self.data_type.parse_str(text)


class DataInputView(QTreeView):
    _args_input = None

    def __init__(self, key, data_type, new_display, parent):
        super().__init__(parent)
        self.key = key
        self.data_type = data_type
        self.new_display = new_display

        self.model = QStandardItemModel()
        # set tree view header
        self.model.setHorizontalHeaderItem(0, QStandardItem("Key"))
        self.model.setHorizontalHeaderItem(1, QStandardItem("Value"))
        self.model.setHorizontalHeaderItem(2, QStandardItem("Type"))
        self.setModel(self.model)

        # self.setItemDelegate()
        self.model.itemChanged.connect(self.data_changed)
        self.expandAll()

    @classmethod
    def get_instance(cls, *args):
        if not cls._args_input:
            cls._args_input = DataInputView(*args)
        return cls._args_input

    def data_changed(self, item):
        print(item)

    def add_data(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    data_input = ArgsInputDialog('test', dict, 'old_value', callable)
    # data_input.resize(675, 250)
    data_input.show()

    sys.exit(app.exec_())
