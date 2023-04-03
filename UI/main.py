import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap, QImage, QColor
from Assets import StyleSheets

app = QApplication(sys.argv)

def recolorPixmap(pixmap: QPixmap, color: QColor):
    tmpImage = pixmap.toImage()

    for x in range(tmpImage.width()):
        for y in range(tmpImage.height()):
            tmpImage.setPixelColor(x, y, QColor(color.red(), color.green(), color.blue(), tmpImage.pixelColor(x, y).alpha()))

    return QPixmap.fromImage(tmpImage)

class QTitleBar(QLabel):
    def __init__(self, window: QMainWindow):
        super(QTitleBar, self).__init__()
        self.parentWindow = window
        self.pressOffset = None

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressOffset = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.pressOffset is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.parentWindow.move(self.parentWindow.pos() + event.pos() - self.pressOffset)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.pressOffset = None
        super().mouseReleaseEvent(event)

class QTitleButton(QLabel):
    def __init__(self, TitleBar: QLabel, pos: int, selectedColor: QColor, selectedBgColor: QColor):
        super(QTitleButton, self).__init__()

        self.setStyleSheet("background-color: red;") #+ StyleSheets.titleButton)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        buttonHeight = round(TitleBar.height() * 1.6) #- TitleBar.layout().getContentsMargins()[1] - TitleBar.layout().getContentsMargins()[3]
        self.setFixedWidth(buttonHeight)
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        TitleBar.layout().addWidget(self, pos)

        self.selectedColor = selectedColor
        self.selectedBgColor = selectedBgColor

    def enterEvent(self, *args, **kwargs):
        self.setPixmap(recolorPixmap(self.pixmap(), self.selectedColor))
        self.setStyleSheet("background-color: rgb(255, 0, 0);")

    def leaveEvent(self, *args, **kwargs):
        self.setPixmap(recolorPixmap(self.pixmap(), StyleSheets.titlebarImageColor))
        self.setStyleSheet("background-color: transparent;")



class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # Adds font to database
        QFontDatabase.addApplicationFont("Assets/Fonts/Sublima-ExtraBold.otf")
        self.PropertyFont = QFont("Sublima ExtraBold", 18)

        # Defines starting size and minimum size for main window
        divFactor = 3
        divFactor = int(round(divFactor))
        self.screenSize = app.primaryScreen().geometry()
        self.resize(self.screenSize.width() // divFactor, self.screenSize.height() // divFactor)
        self.setMinimumSize(self.screenSize.width() // divFactor, self.screenSize.height() // divFactor)

        # Creates central widget
        self.CentralWidget = QWidget()
        self.CentralWidget.setStyleSheet(StyleSheets.darkBox)
        self.CentralWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(self.CentralWidget)

        # Set window attributes
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Sets up main window's layout
        self.MainLayout = QGridLayout()
        self.CentralWidget.setLayout(self.MainLayout)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.MainLayout.setSpacing(0)
        self.MainLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)

        # Creates custom title bar
        self.TitleEdgeOffset = 0

        self.TitleBar = QTitleBar(self)
        self.TitleBar.setStyleSheet(StyleSheets.titleBar)
        self.TitleBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.TitleBar.setFixedHeight(self.screenSize.height() // 50)
        self.TitleBar.setLayout(QHBoxLayout())
        self.TitleBar.layout().setContentsMargins(self.TitleEdgeOffset, self.TitleEdgeOffset, self.TitleEdgeOffset, self.TitleEdgeOffset)
        self.TitleBar.layout().setSpacing(self.TitleEdgeOffset)
        self.MainLayout.addWidget(self.TitleBar, 0, 0, 1, 2)

        # Creates title and icon
        self.Title = QLabel()
        self.Logo = QPixmap("Assets/Icons/Logo.png")
        self.Logo = self.Logo.scaledToHeight(self.TitleBar.height() - self.TitleEdgeOffset * 2)
        self.Title.setFixedSize(self.TitleBar.height() - self.TitleEdgeOffset * 2, self.TitleBar.height() - self.TitleEdgeOffset * 2)
        self.Title.setPixmap(self.Logo)
        self.TitleBar.layout().addWidget(self.Title, 0)

        self.Title = QLabel("Macro Ultimate")
        self.Title.setFont(QFont("Sublima ExtraBold", 10))
        self.Title.setStyleSheet(StyleSheets.lightText)
        self.TitleBar.layout().addWidget(self.Title, 0)

        self.TitleBar.layout().insertSpacing(2, self.screenSize.width())

        # Creates custom titlebar buttons
        self.ExitButton = QTitleButton(self.TitleBar, 0, QColor(255, 255, 255), QColor(255, 0, 16))
        self.CrossIcon = QPixmap("Assets/Icons/close.svg")
        self.CrossIcon = self.CrossIcon.scaledToHeight(round(self.TitleBar.height() / 1.5))
        self.CrossIcon = recolorPixmap(self.CrossIcon, QColor(255, 255, 255))
        self.ExitButton.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ExitButton.setPixmap(self.CrossIcon)
        self.ExitButton.mousePressEvent = exit

        #self.MinimizeButton = QTitleButton(self.TitleBar, 0)


        # Sets up container for command nodes
        self.NodeContainer = QWidget(self.CentralWidget)
        self.NodeContainer.setStyleSheet(StyleSheets.lightBox)
        self.NodeContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.NodeContainer.setFixedWidth(self.width() // 3)
        self.NodeContainer.setLayout(QVBoxLayout())

        self.MainLayout.addWidget(self.NodeContainer, 1, 0, 1, 1)

        # Sets up container for command nodes' properties
        self.PropertyContainer = QWidget(self.CentralWidget)
        self.PropertyContainer.setStyleSheet(StyleSheets.darkBox)
        self.PropertyContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.PropertyContainer.setLayout(QVBoxLayout())
        self.PropertyContainer.layout().setContentsMargins(10, 0, 10, 10)

        # Sets up property section elements
        self.PropertyTitle = QLabel("Properties")
        self.PropertyTitle.setFont(self.PropertyFont)
        self.PropertyTitle.setStyleSheet(StyleSheets.titleText)
        self.PropertyContainer.layout().addWidget(self.PropertyTitle)

        self.PropertyBox = QWidget(self.CentralWidget)
        self.PropertyBox.setStyleSheet(StyleSheets.lightBox + StyleSheets.roundedParam)
        self.PropertyBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.PropertyBox.setLayout(QVBoxLayout())
        self.PropertyContainer.layout().addWidget(self.PropertyBox, 1)

        self.MainLayout.addWidget(self.PropertyContainer, 1, 1, 1, 1)

        # Creates custom scaling corner
        self.gripBorderOffset = 20

        self.CornerGripWidget = QSizeGrip(self.CentralWidget)
        self.CornerGripWidget.setStyleSheet("background-color: rgb(255, 0, 0);")

    def exit(self, event):
        app.quit()

    def resizeEvent(self, event) -> None:
        # Reposition scaling corner
        self.CornerGripWidget.setGeometry(self.width() - self.gripBorderOffset, self.height() - self.gripBorderOffset, self.gripBorderOffset, self.gripBorderOffset)



def main():
    window = MainWindow()
    window.setWindowTitle('AutoClicker Ultimate')

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()