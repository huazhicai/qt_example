

class SpinBoxDelegate(QItemDelegate):
    def __init__(self, column, parent=None):
        super().__init__(parent)
        self.column = column 

    def paint(self, painter, option, index):
        if index.column() == self.column:
            value = index.model().data(index, Qt.DisplayRole)
            option.displayALignment = Qt.AlignRight | Qt.AlignVCenter
            self.drawDisplay(painter, option, option.rect, str(value) if value is not None else None)
            self.drawFoucs(painter, option, option.rect)
        else:
            super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        if index.column() == self.column:
            spinBox = QSpinBox(parent)
            spinBox.setRange(0, 2000)
            spinBox.editingFinished.connect(self.commitAndCloseEditor)
            return spinBox
        else:
            return super().createEditor(paint, option, index)

    def commitAndCloseEditor(self):
        spinBox = self.sender()
        self.commitData.emit(spinBox)
        self.closeEditor.emit(spinBox)

    def setEditorData(self, editor, index):
        if index.column() == self.column:
            value = index.model().data(index, Qt.DisplayRole)
            editor.setValue(value if value is not None else 0)
        else:
            super().setEditorData(editor, index)


class TableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel(self)
        self.setMode(self.model)
        spinBoxDelegate = SpinBoxDelegate(1)
        self.setItemDelegate(spinBoxDelegate)