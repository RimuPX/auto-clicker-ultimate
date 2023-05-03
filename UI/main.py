import sys

from PyQt6.QtGui import QFontDatabase, QCursor
from PyQt6.QtWidgets import QMainWindow

from Assets.Extensions.QProperties import *
from Assets.Extensions.QNodes import *
from Assets.StyleSheets import *
from Assets.Extensions.Singleton import *

# Creates app
app = QApplication(sys.argv)

# Adds font to database
QFontDatabase.addApplicationFont("Assets/Fonts/Sublima-ExtraBold.otf")

class MainWindow(Singleton, QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()

        # Defines starting size and minimum size for main window
        self.windowScaleFactor = 3
        self.screenSize = app.primaryScreen().geometry()
        self.resize(self.screenSize.width() // self.windowScaleFactor, self.screenSize.height() // self.windowScaleFactor)
        self.setMinimumSize(self.screenSize.width() // self.windowScaleFactor, self.screenSize.height() // self.windowScaleFactor)

        # Creates central widget
        CentralWidget = QWidget(self)
        CentralWidget.setObjectName("CentralWidget")
        CentralWidget.setStyleSheet(MainSheet.Sheet)
        CentralWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(CentralWidget)

        # Sets up main window's layout
        self.MainLayout = QGridLayout(self)
        self.centralWidget().setLayout(self.MainLayout)
        self.MainLayout.setContentsMargins(10, 10, 10, 10)
        self.MainLayout.setSpacing(10)

        # Creates a panel with context buttons
        #self.MainLayout.addWidget(self.ActionPanel, 1, 0, 1, 1)

        # Sets up container for command nodes' properties
        self.PropertyBox = QPropertyBox()
        print(QPropertyBox.getInstance())
        self.MainLayout.addWidget(self.PropertyBox, 0, 1, self.MainLayout.rowCount(), 1)

        # Sets up container for nodes
        self.NodeBox = QNodeBox()
        self.MainLayout.setRowStretch(0, 7)
        self.MainLayout.addWidget(self.NodeBox, 0, 0, 1, 1)

        # Key press control
        self.controlDown = False
        self.shiftDown = False

        self.mousePressPos = None
        self.mouseHoldPos = None


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Control:
            self.controlDown = True
        elif event.key() == Qt.Key.Key_Shift:
            self.shiftDown = True
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Control:
            self.controlDown = False
        elif event.key() == Qt.Key.Key_Shift:
            self.shiftDown = False
        super().keyReleaseEvent(event)

    def mousePressEvent(self, event):
        self.mousePressPos = self.mapFromGlobal(QCursor().pos())

    def mouseMoveEvent(self, event):
        self.mouseHoldPos = event.pos()

        nodes = []
        for nodeIndex in range(0, self.NodeBox.NodeList.layout().count()):
            nodes.append(self.NodeBox.NodeList.layout().itemAt(nodeIndex).widget())
        for node in nodes:
            absNodePos = self.NodeBox.NodeList.mapTo(self, QPoint(node.x(), node.y()))
            if boxesOverlap(self.mousePressPos,
                            self.mouseHoldPos,
                            absNodePos,
                            QPoint(absNodePos.x() + node.width(), absNodePos.y() + node.height())):
                self.NodeBox.selectNodes([node])
            else:
                self.NodeBox.deselectNodes([node])

        loop = QLoop.getInstance()
        absLoopPos = self.NodeBox.mapTo(self, QPoint(loop.x(), loop.y()))
        if boxesOverlap(self.mousePressPos,
                        self.mouseHoldPos,
                        absLoopPos,
                        QPoint(absLoopPos.x() + loop.width(), absLoopPos.y() + loop.height())):
            self.NodeBox.selectNodes([loop])
        else:
            self.NodeBox.deselectNodes([loop])


    def mouseReleaseEvent(self, event):
        self.mousePressPos = None
        self.mouseHoldPos = None

def main():
    window = MainWindow()
    window.setWindowTitle('AutoClicker Ultimate')

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
