import  sys

from PyQt6.QtGui import QFontDatabase

from Assets.Extensions.QNodes import *
from Assets.Extensions.QProperties import *

# Creates app
app = QApplication(sys.argv)

# Adds font to database
QFontDatabase.addApplicationFont("Assets/Fonts/Sublima-ExtraBold.otf")

class MainWindow(QMainWindow):

    __instance = None
    hasInstance = False

    def __new__(cls, *args):
        if not cls.__instance:
            cls.__instance = super(QMainWindow, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if MainWindow.hasInstance: return

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

        # Sets up container for nodes
        self.NodeBox = QNodeBox()
        self.MainLayout.setRowStretch(0, 7)
        self.MainLayout.addWidget(self.NodeBox, 0, 0, 1, 1)

        # Creates a panel with context buttons
        self.ActionPanel = QActionPanel(self.centralWidget())
        self.MainLayout.addWidget(self.ActionPanel, 1, 0, 1, 1)

        # Sets up container for command nodes' properties
        self.PropertyBox = QPropertyBox()
        self.MainLayout.addWidget(self.PropertyBox, 0, 1, self.MainLayout.rowCount(), 1)

        # Key press control
        self.controlDown = False
        self.shiftDown = False
        self.lmbDown = False

        MainWindow.hasInstance = True

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
        self.lmbDown = True
        print('pressed')
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.lmbDown = False
        print('unpressed')
        super().mouseReleaseEvent(event)

def main():
    window = MainWindow()
    window.setWindowTitle('AutoClicker Ultimate')

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()