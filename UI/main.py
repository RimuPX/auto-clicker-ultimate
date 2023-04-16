import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase

from Assets import StyleSheets
from Assets.Extensions.QNodes import *
from Assets.Extensions.HelpfulFuncs import *
from Assets.Extensions.QProperties import *

# Creates app
app = QApplication(sys.argv)

# Adds font to database
QFontDatabase.addApplicationFont("Assets/Fonts/Sublima-ExtraBold.otf")

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # Defines starting size and minimum size for main window
        self.windowScaleFactor = 3
        self.windowScaleFactor = int(round(self.windowScaleFactor))
        self.screenSize = app.primaryScreen().geometry()
        self.resize(self.screenSize.width() // self.windowScaleFactor, self.screenSize.height() // self.windowScaleFactor)
        self.setMinimumSize(self.screenSize.width() // self.windowScaleFactor, self.screenSize.height() // self.windowScaleFactor)

        # Creates central widget
        CentralWidget = QWidget()
        CentralWidget.setObjectName("CentralWidget")
        CentralWidget.setStyleSheet(StyleSheets.MainSheet)
        CentralWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(CentralWidget)

        # Set window attributes
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Sets up main window's layout
        self.MainLayout = QGridLayout()
        self.centralWidget().setLayout(self.MainLayout)
        self.MainLayout.setContentsMargins(10, 10, 10, 10)
        self.MainLayout.setSpacing(10)
        self.MainLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)

        # Sets up container for nodes
        self.NodeBox = QNodeBox(StyleSheets.MainSheet)
        self.MainLayout.setRowStretch(0, 7)
        self.MainLayout.addWidget(self.NodeBox, 0, 0, 1, 1)

        # Creates a panel with context buttons
        self.ActionPanel = QActionPanel(self.centralWidget())

        # Sets up container for command nodes' properties
        self.PropertyBox = QPropertyBox()
        self.MainLayout.addWidget(self.PropertyBox, 0, 1, self.MainLayout.rowCount(), 1)

        setShadow(self.ActionPanel)
        setShadow(self.NodeBox)
        setShadow(self.PropertyBox)

        # Key press control
        self.ControlDown = False

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Control:
            self.ControlDown = True

    def keyReleaseEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Control:
            self.ControlDown = False

def main():
    window = MainWindow()
    window.setWindowTitle('AutoClicker Ultimate')

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()