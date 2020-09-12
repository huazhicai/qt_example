

class MyDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(parent, option, index):
        if index.column() == 3:
            box = QComboBox(parent)
            box.addItems(['优', '良', '差'])
            return box 

    def setEditorData(editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setCurrentText(value)

    def setModelData(editor, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)

    def updateEditorGeometry(editor, option, index):
        editor.setGeometry(option.rect)

class TreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditTriggers(QTreeView.NoEditTriggers)
        self.setSelectionBehavior(QTreeView.SelectRows)
        self.setSelectionMode(QTreeView.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setFocusPolicy(Qt.NoFocus)

        delegate = MyDelegate()
        self.setItemDelegate(delegate)