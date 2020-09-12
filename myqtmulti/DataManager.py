

class DataManager():
    def __init__():
        self.currentJsonObject = None
        self.currentJsonFileUrl = QUrl()
        self.dirty = False 

    def loadFromFile(path):
        if not QFile.exists(path):
            print("File not found: %s" % path, '\n')
            return False
        currentJsonFileUrl = QUrl.fromLocalFile(path)
        the_file = QFile(currentJsonFileUrl.toLocalFile())
        if not the_file.open(QIODevice.ReadOnly|QIODevice.Text):
            print("Cnt't open file: {}".format(path))
            return False


    def saveToFile():
        pass 

    def savePathFile(path):
        pass

    def currentFileExists():
        return QFile.exists(self.currentJsonFileUrl.toLocalFile())

    def getFileName():
        return currentJsonFileUrl.fileName()

    def setDirty(d=False):
        self.dirty = d  

    def isDirty():
        pass
