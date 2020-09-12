from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QAction

from myqtmulti.MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.theModel = QStandardItemModel()
        theItemDelegate = RixJsonItemDelegate()

        self.theModel.setHorizontalHeaderItem(0, QStandardItem('Key'))
        self.theModel.setHorizontalHeaderItem(1, QStandardItem('Value'))
        self.theModel.setHorizontalHeaderItem(2, QStandardItem('Type'))

        # 设置TREE VIEW使用的模型为StandarItemModel
        self.treeView.setModel(theModel)
        # 设置Tree View使用的委托为自定义的委托
        self.treeView.setItemDelegate(theItemDelegate)

        self.theModel.itemChanged.connect(self.treeDataChanged)

        self.openButton.clicked.connect(self.openFile)
        self.saveButton.clicked.connect(self.saveFile)
        self.saveAnotherFile.clicked.connect(self.saveAnotherFile)

        self.menuEdit.triggered.connect(self.onMenuActionTrigger)
        self.menuFile.triggered.connect(self.onMenuActionTrigger)

        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.CustomContextMenuRequested.connect(self.showTreeViewMenu)

        self.menuEdit.aboutToShow.connect(self.aboutToShowEditMenu)

    def treeDataChanged(self, item: 'QStandardItem'):
        s = QStack()
        if item.column() == 0:
            i = self.theModel.indexFromItem(item)
        else:
            i = self.theModel.indexFromItem(item).siblingAtColumn(0)
        while i.isValid():
            o = DataManager.get_instance().getCurrentJsonObject()
            p = None
        while not s.isEmpty():
            index = s.pop()
            p = o
            o = DataManager.get_instance().getChild(index.row())
                

    def openFile(self):
        pass

    def saveFile(self):
        pass

    def saveAnotherFile(self):
        pass

    def onMenuActionTrigger(self, action: 'QAction'):
        pass

    def showTreeViewMenu(self, point: 'QPoint'):
        self.menuEdit.exec(QCursor.pos())

    def aboutToShowEditMenu(self):
        index = self.treeView.selectionModel.currentIndex()
        self.actionAddChild.setVisible(index.isValid() & (index.siblingAtColumn(2).data(Qt.DisplayRole)))

    def updateTreeModel(self):
        pass

    def addRixJsonItem(self, asChild=False, key="key", value="value", type=str):
        index = self.treeView.selectionModel().currentIndex()

        if not index.isValid():
            o = DataManager.get_instance().getCurrentJsonObject()
            o.setType(type)
            o.addChild(new_o)  # ????

            self.updateTreeModel()
            self.textBrowser.setText(DataManager.get_instance().getCurrentJsonObject())
            DataManager.get_instance().setDirty(True)
            self.setWindowTitle("RixJsonEditor | " + DataManager.get_instance().getFileName() + "*")
            return

        item = self.theModel.itemFromIndex(index)
        s = QStack()
        if item.column() ==0:
            i = self.theModel.indexFromItem(item)
        else:
            i = self.theModel.indexFromItem(item).siblingAtColumn(0)
        while i.isValid:
            s.push(i)
            i = i.parent()
        o = DataManager.get_instance().getCurrentJsonObject()
        p = None
        while not s.isEmpty():
            index = s.pop()
            p = o 
            o = DataManager.get_instance().getChild(index.row())

        if asChild:
            o.addChild(new_o)
        else:
            if p !=None:
                os = p.getChildren()
                pos = index.row()
                os.insert(os.begin()+pos+1, new_o)  # ???
        self.updateTreeModel()
        self.textBrowser.setText(DataManager.get_instance().getCurrentJsonObject())
        DataManager.get_instance().setDirty(True)
        self.setWindowTitle("RixJsonEditor | " + DataManager.get_instance().getFileName() + "*")

    def deleteRixJsonItem(self):
        index = self.treeView.selectionModel().currentIndex()
        if not index.isValid():
            return
        item = self.theModel.itemFromIndex(index)
        s = QStack()
        if item.column() == 0:
            i = self.theModel.indexFromItem(item)
        else:
            i = self.theModel.indexFromItem(item).siblingAtColumn(0)
        while i.isValid():
            s.push(i)            
            i = i.parent()
        o = DataManager.get_instance().getCurrentJsonObject()
        p = None
        while not s.isEmpty():
            index = s.pop()
            p = o
            o = DataManager.get_instance().getChild(index.row())
        if p!=None:
            os = p.getChildren()
            os.erase(os.begin() + index.row())

            self.updateTreeModel()
            self.textBrowser.setText(DataManager.get_instance().getCurrentJsonObject())
            DataManager.get_instance().setDirty(True)
            self.setWindowTitle("RixJsonEditor | " + DataManager.get_instance().getFileName() + "*")


    def expandAll(self):
        self.treeView.expandAll

    def collapseAll(self):
        self.treeView.collapseAll() 