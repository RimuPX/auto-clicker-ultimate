import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from ui import *

app = QApplication(sys.argv)
class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # Creates central widget
        CentralWidget = QWidget()
        self.setCentralWidget(CentralWidget)

        # Removes default title bar and borders
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Defines starting size and minimum size for main window
        divFactor = 3
        divFactor = int(round(divFactor))
        screenSize = app.primaryScreen().geometry()
        self.resize(screenSize.width() // divFactor, screenSize.height() // divFactor)
        self.setMinimumSize(screenSize.width() // divFactor, screenSize.height() // divFactor)

        # Sets up main window's layout
        self.MainLayout = QGridLayout()
        CentralWidget.setLayout(self.MainLayout)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.MainLayout.setSpacing(0)
        self.MainLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)

        # Creates custom title bar
        self.TitleBar = QWidget(self)
        self.TitleBar.setStyleSheet("background-color: rgb(38, 38, 50);")
        self.TitleBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.TitleBar.setFixedHeight(screenSize.height() // 50)
        self.TitleBar.setLayout(QVBoxLayout())

        self.MainLayout.addWidget(self.TitleBar, 0, 0, 1, 2)

        # Sets up container for command nodes
        self.NodeContainer = QWidget(self)
        self.NodeContainer.setStyleSheet("background-color: rgb(35, 35, 47);")
        self.NodeContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.NodeContainer.setFixedWidth(self.width() // 3)
        self.NodeContainer.setLayout(QVBoxLayout())

        self.MainLayout.addWidget(self.NodeContainer, 1, 0, 1, 1)

        # Sets up container for command nodes' properties
        self.PropertyContainer = QWidget(self)
        self.PropertyContainer.setStyleSheet("background-color: rgb(32, 32, 42);")
        self.PropertyContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.PropertyContainer.setLayout(QVBoxLayout())

        self.MainLayout.addWidget(self.PropertyContainer, 1, 1, 1, 1)

        # Creates custom scaling corner
        self.gripBorderOffset = 20

        self.CornerGripWidget = QSizeGrip(self)
        self.CornerGripWidget.setStyleSheet("background-color: rgb(255, 0, 0);")

        # Declares window dragging variables
        self.pressOffset = None

    def resizeEvent(self, event) -> None:
        # Reposition scaling corner
        self.CornerGripWidget.setGeometry(self.width() - self.gripBorderOffset, self.height() - self.gripBorderOffset, self.gripBorderOffset, self.gripBorderOffset)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressOffset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.pressOffset is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.pressOffset)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.pressOffset = None
        super().mouseReleaseEvent(event)




def main():
    window = MainWindow()
    window.setWindowTitle('AutoClicker Ultimate')

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()