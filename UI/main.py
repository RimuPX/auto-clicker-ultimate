import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QFontDatabase
from Assets import StyleSheets

app = QApplication(sys.argv)

# Check if title is clicked
def inBoxBound(position: QPoint, widget: QWidget, centralWidget: QWidget) -> bool:
    x, y = position.x(), position.y()
    h, w = widget.geometry().height(), widget.geometry().width()
    pos = widget.mapTo(centralWidget, QPoint(widget.geometry().x(), widget.geometry().y()))

    if pos.x() < x < pos.x() + w and pos.y() < y < pos.y() + h:
        return True

    return False

class ClickableWidget(QWidget):
    def __init__(self, window):
        super().__init__()

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # Defines starting size and minimum size for main window
        divFactor = 3
        divFactor = int(round(divFactor))
        screenSize = app.primaryScreen().geometry()
        self.resize(screenSize.width() // divFactor, screenSize.height() // divFactor)
        self.setMinimumSize(screenSize.width() // divFactor, screenSize.height() // divFactor)

        # Creates central widget
        self.CentralWidget = QWidget()
        self.CentralWidget.setStyleSheet(StyleSheets.darkBg)
        self.CentralWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(self.CentralWidget)

        # Set window attributes
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        # self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Sets up main window's layout
        self.MainLayout = QGridLayout()
        self.CentralWidget.setLayout(self.MainLayout)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.MainLayout.setSpacing(0)
        self.MainLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)




        self.p = ClickableWidget(self)
        self.p.setVisible(True)
        self.p.show()
        self.p.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.p.setStyleSheet("background-color: rgb(0, 0, 255);")
        self.MainLayout.addWidget(self.p)




        # Creates custom title bar
        self.TitleBar = QWidget(self.CentralWidget)
        self.TitleBar.setStyleSheet(StyleSheets.titleBar)
        self.TitleBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.TitleBar.setFixedHeight(screenSize.height() // 50)
        self.TitleBar.setLayout(QHBoxLayout())

        self.MainLayout.addWidget(self.TitleBar, 0, 0, 1, 2)

        # Sets up container for command nodes
        self.NodeContainer = QWidget(self.CentralWidget)
        self.NodeContainer.setStyleSheet(StyleSheets.lightBg)
        self.NodeContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.NodeContainer.setFixedWidth(self.width() // 3)
        self.NodeContainer.setLayout(QVBoxLayout())

        self.MainLayout.addWidget(self.NodeContainer, 1, 0, 1, 1)

        # Sets up container for command nodes' properties
        self.PropertyContainer = QWidget(self.CentralWidget)
        self.PropertyContainer.setStyleSheet(StyleSheets.darkBg)
        self.PropertyContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.PropertyContainer.setLayout(QVBoxLayout())
        self.PropertyContainer.layout().setContentsMargins(10, 0, 10, 10)

        QFontDatabase.addApplicationFont("Assets/Fonts/Sublima-ExtraBold.otf")
        self.PropertyFont = QFont("Sublima ExtraBold", 18)
        self.PropertyTitle = QLabel("Properties")
        self.PropertyTitle.setFont(self.PropertyFont)
        self.PropertyTitle.setStyleSheet(StyleSheets.darkBg)
        self.PropertyContainer.layout().addWidget(self.PropertyTitle)

        self.PropertyBox = QWidget(self.CentralWidget)
        self.PropertyBox.setStyleSheet(StyleSheets.lightBg + StyleSheets.roundedBox)
        self.PropertyBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.PropertyBox.setLayout(QVBoxLayout())
        self.PropertyContainer.layout().addWidget(self.PropertyBox, 1)

        self.MainLayout.addWidget(self.PropertyContainer, 1, 1, 1, 1)

        # Creates custom scaling corner
        self.gripBorderOffset = 20

        self.CornerGripWidget = QSizeGrip(self.CentralWidget)
        self.CornerGripWidget.setStyleSheet("background-color: rgb(255, 0, 0);")

        # Declares window dragging variables
        self.pressOffset = None

    def resizeEvent(self, event) -> None:
        # Reposition scaling corner
        self.CornerGripWidget.setGeometry(self.width() - self.gripBorderOffset, self.height() - self.gripBorderOffset, self.gripBorderOffset, self.gripBorderOffset)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton and inBoxBound(event.pos(), self.TitleBar, self.centralWidget()):
            self.pressOffset = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.pressOffset is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.pressOffset)
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