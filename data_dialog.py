import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import *
from graph.node_def.data_type import Bool, Int, Float, Str, List, Dict, Any, Event


class ArgsInputDialog(QDialog):
    def __init__(self, title, data_type, old_value, doneChangeCallback, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.data_type = data_type
        self.old_value = old_value
        self.doneChangeCallback = doneChangeCallback

        # self.newDisplay = QTextBrowser()
        self.newDisplay = QTextEdit()
        self.newInput = ArgsInput.get_instance(data_type, self.newDisplay, self)
        self.newInput.add_top_data()

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
        layout.addWidget(self.newDisplay, 0, 3, 4, 3)
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


class ArgsInput(QTreeWidget):
    args_input = None

    def __init__(self, data_type, new_display, parent):
        super().__init__(parent)
        self.data_type = data_type
        self.new_display = new_display

        self.setColumnCount(3)
        self.setColumnWidth(2, 0)
        self.resizeColumnToContents(2)
        self.setColumnWidth(2, 200)
        self.header().setSectionResizeMode(QHeaderView.Interactive)
        # self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.headerItem().setText(0, "key")
        self.headerItem().setText(1, "value")
        self.headerItem().setText(2, "type")

    @classmethod
    def get_instance(cls, *args):
        if not cls.args_input:
            cls.args_input = ArgsInput(*args)
        return cls.args_input

    def add_top_data(self):
        self.child = TopDataItem.get_instance(self.data_type, self)
        # self.itemChanged.connect(self.display_data)

    def check_data_type(self, data_type, value):
        if data_type == 'int' and value and value.isnumeric():
            value = eval(value)
            return type(value) == int
        elif data_type == 'float':
            try:
                value = eval(value)
            except:
                pass
            return type(value) == float or int
        elif data_type == 'bool':
            value = eval(value)
            return type(value) == bool
        elif data_type == 'Dict':
            return type(value) == dict
        elif data_type == 'str':
            return type(value) == str
        elif data_type == 'List':
            return type(value) == list
        elif data_type == 'any':
            return type(value) in [int, float, bool, str, List, object, Dict]

    def display_data(self, item, p_int):
        data_type = self.child.text(2)
        val = self.child.text(1)
        if data_type == 'str' and self.check_data_type(data_type, val):
            self.new_display.setPlainText('"' + val + '"')
        elif data_type == 'int' and self.check_data_type(data_type, val):
            self.new_display.setPlainText(val)
        elif data_type == 'float' and self.check_data_type(data_type, val):
            self.new_display.setPlainText(str(float(val)))
        elif data_type == 'bool' and self.check_data_type(data_type, val):
            self.new_display.setPlainText(val)

        elif data_type == 'List':
            val = self.get_val(self.child)
            self.new_display.setPlainText(str(val))

        elif data_type == 'Dict':
            val = self.get_val(self.child)
            self.new_display.setPlainText(str(val))

    def get_val(self, parent):
        child_count = parent.childCount()
        if parent.data_type == List:
            value = []
        else:
            value = {}
        for i in range(child_count - 1):
            item = parent.child(i)
            key = item.text(0)
            if key == '':
                continue
            if item.data_type in (List, Dict):
                val = self.get_val(item)
            else:
                val = item.text(1)
                if item.data_type != str:
                    val = eval(val)
                if item.data_type == float:
                    print(val)
                    # val = float(val)
            if isinstance(value, list):
                value.append(val)
            elif isinstance(value, dict):
                value.update({key: val})
        return value


class BaseDataItem(QTreeWidgetItem):
    def __init__(self, data_type, parent):
        super().__init__(parent)

        self.parent = parent
        self.data_type = data_type
        self.setExpanded(True)
        self.btn = None

    def initSingleElement(self):
        self.setText(0, 'field')
        self.setForeground(0, QBrush(QColor(Qt.gray)))
        self.setText(1, 'value')
        self.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)

    def initContainerElement(self, data_type, num=0):
        self.setText(0, '%s' % data_type.__name__)
        if data_type == Dict:
            self.setText(1, '{%s}' % num)
        elif data_type == List:
            self.setText(1, '[%s]' % num)
        elif data_type == tuple:
            self.setText(1, '(%s)' % num)

        self.setForeground(1, QBrush(QColor(Qt.gray)))
        self.add_button(data_type)

    def add_button(self, data_type):
        child = QTreeWidgetItem(self)
        self.btn = child
        child.setFlags(Qt.ItemIsSelectable)
        child.setDisabled(True)
        self.addChild(child)
        ArgsInput.args_input.setItemWidget(child, 0, AddButton('+', child, data_type))

    def del_button(self):
        index = self.childCount()
        child = self.child(index - 1)
        if child and child.text(0) == '':
            self.takeChild(index - 1)
            self.btn = None


class TopDataItem(BaseDataItem):
    top_data_item = None

    def __init__(self, data_type, parent=None):
        super().__init__(data_type, parent)

        brush = QBrush(QColor(55, 55, 55))
        brush.setStyle(Qt.NoBrush)
        self.setForeground(0, brush)

        self.setText(2, data_type.__name__)
        self.setForeground(0, QBrush(QColor(Qt.gray)))
        self.setForeground(2, QBrush(QColor(Qt.gray)))

        if data_type in (str, int, float):
            self.initSingleElement()
        elif data_type in (Dict, List):
            self.initContainerElement(data_type)

    @classmethod
    def get_instance(cls, *args):
        if not cls.top_data_item:
            cls.top_data_item = TopDataItem(*args)
        return cls.top_data_item


class DataItem(BaseDataItem):
    def __init__(self, parent, data_type=str):
        super().__init__(data_type, parent)
        self.setExpanded(True)

        self.brush = QBrush(Qt.gray)
        # self.initContainerElement(data_type)
        self.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
        self.combine_btn = CombineButton(self)
        ArgsInput.args_input.setItemWidget(self, 2, self.combine_btn)

    def change_btn_text(self, text):
        self.combine_btn.setCurrentText(text)

    def change_data_type(self, data_type):
        self.data_type = eval(data_type)
        if data_type in ('str', 'int', 'float'):
            super().del_button()
        elif data_type == 'List':
            if self.parent.data_type == List:
                self.setText(0, 'field')
                self.setText(1, '[0]')
                self.parent.setText(1, '[%s]' % (self.parent.childCount() - 1))
            elif self.parent.data_type == Dict:
                self.setText(1, '[0]')
            self.setForeground(1, self.brush)
            if not self.btn:
                super().add_button(eval(data_type))

        elif data_type == 'Dict':
            if self.parent.data_type == List:
                self.parent.setText(1, '[%s]' % (self.parent.childCount() - 1))
                self.setText(1, '{0}')
            elif self.parent.data_type == Dict:
                self.setText(1, '{0}')
            self.setForeground(1, self.brush)
            if not self.btn:
                super().add_button(eval(data_type))

    def add_data_element(self, data_type):
        self.initContainerElement(data_type)

    def initSingleElement(self):
        super().initSingleElement()

    def initContainerElement(self, data_type, num=0):
        assert data_type in (str, int, float, Dict, List, set, tuple)
        if data_type == Dict:
            self.setText(0, 'field')
            self.setText(1, 'value')
        elif data_type == List:
            self.setText(0, str(self.parent.childCount() - 1))
            self.setText(1, 'value')
            self.setForeground(0, self.brush)
        elif data_type in (str, int, float):
            super().initSingleElement()
        else:
            pass

    def clones(self, data_type):
        # super().clone()
        data_item = DataItem(None, data_type)
        # data_item.clone()
        data_item.add_data_element(data_type)
        return data_item


class AddButton(QPushButton):

    def __init__(self, text, parent, data_type):
        super().__init__(text)

        self.parent = parent.parent()
        self.myself = parent
        # self.button = btn
        self.data_type = data_type

        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(20, 20)
        self.setToolTip('添加')
        self.clicked.connect(self.add_data_item)

    def add_data_item(self):
        child = DataItem(None, str)
        child.parent = self.parent
        child.add_data_element(self.data_type)

        index = self.parent.indexOfChild(self.myself)
        self.parent.insertChild(index, child)

        ArgsInput.args_input.setItemWidget(child, 2, CombineButton(child))
        self.update_parent()

    def update_parent(self):
        if self.data_type == Dict:
            self.parent.setText(1, '{%d}' % (self.parent.childCount() - 1))
        elif self.data_type == List:
            if self.parent.data_type == List:
                self.parent.setText(1, '[%s]' % (self.parent.childCount() - 1))
        self.parent.setForeground(1, QBrush(QColor(Qt.gray)))


class SwitchDataTypeButton(QComboBox):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent.parent
        self.myself = parent
        self.addItems(['str', 'int', 'float', 'List', 'Dict'])
        self.setFixedSize(45, 20)
        self.setContentsMargins(0, 0, 0, 0)

        self.currentTextChanged.connect(self.changeDataType)

    def changeDataType(self, text):
        print(self.myself.text(0))
        print(self.myself.text(1))
        self.myself.change_data_type(text)
        ArgsInput.args_input.itemChanged.emit(self.myself, 1)


class CombineButton(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent.parent
        self.myself = parent

        self.switch_data_btn = SwitchDataTypeButton(parent)

        copy_btn = QPushButton('c')
        copy_btn.setFixedSize(20, 20)
        copy_btn.clicked.connect(self.copy_item_data)
        del_btn = QPushButton('x')
        del_btn.setFixedSize(20, 20)
        del_btn.clicked.connect(self.del_item_data)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.switch_data_btn)
        layout.addWidget(copy_btn)
        layout.addWidget(del_btn)

        self.setLayout(layout)
        self.setFixedSize(120, 20)
        self.setContentsMargins(0, 0, 0, 0)

    def setCurrentText(self, text):
        self.switch_data_btn.setCurrentText(text)

    def copy_item_data(self):
        index = self.parent.indexOfChild(self.myself)
        # copy_item = self.myself.clones(self.myself.data_type)
        copy_item = self.myself.clones(self.myself.data_type)
        copy_item.parent = self.parent
        self.parent.insertChild(index, copy_item)
        ArgsInput.args_input.setItemWidget(copy_item, 2, CombineButton(copy_item))
        self.update_parent()

    def del_item_data(self):
        self.parent.removeChild(self.myself)
        self.update_parent()

    def update_parent(self):
        if self.parent.data_type == Dict:
            self.parent.setText(1, '{%d}' % (self.parent.childCount() - 1))
        elif self.parent.data_type == List:
            self.parent.setText(1, ' [%s]' % (self.parent.childCount() - 1))
            child_count = self.parent.childCount()
            for i in range(child_count - 1):
                self.parent.child(i).setText(0, str(i))
        self.parent.setForeground(1, QBrush(QColor(Qt.gray)))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    data_input = ArgsInputDialog('test', Dict, 'old_value', callable)
    data_input.resize(675, 250)
    data_input.show()

    sys.exit(app.exec_())
