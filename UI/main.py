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
    def __init__(self, TitleBar: QLabel, pixmapPath: str):
        super(QTitleButton, self).__init__()

        buttonHeight = round(TitleBar.height() * 1.6)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(buttonHeight)
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.setPixmap(QPixmap(pixmapPath))
        self.setPixmap(self.pixmap().scaledToHeight(round(TitleBar.height() / 1.5)))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        TitleBar.layout().addWidget(self)

    def enable(self):
        self.setPixmap(recolorPixmap(self.pixmap(), StyleSheets.titleBarSelectedImageColor))
    def enterEvent(self, *args, **kwargs):
        self.enable()

    def disable(self):
        self.setPixmap(recolorPixmap(self.pixmap(), StyleSheets.titlebarImageColor))
    def leaveEvent(self, *args, **kwargs):
        self.disable()



class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # Adds font to database
        QFontDatabase.addApplicationFont("Assets/Fonts/Sublima-ExtraBold.otf")
        self.PropertyFont = QFont("Sublima ExtraBold", 18)

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
        #self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Sets up main window's layout
        self.MainLayout = QGridLayout()
        self.centralWidget().setLayout(self.MainLayout)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.MainLayout.setSpacing(0)
        self.MainLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)

        # Creates custom title bar
        self.titleEdgeOffset = 0
        self.titleBarScaleFactor = 50

        self.TitleBar = QTitleBar(self)
        self.TitleBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.TitleBar.setFixedHeight(self.screenSize.height() // self.titleBarScaleFactor)
        self.TitleBar.setLayout(QHBoxLayout())
        self.TitleBar.layout().setContentsMargins(self.titleEdgeOffset, self.titleEdgeOffset, self.titleEdgeOffset, self.titleEdgeOffset)
        self.TitleBar.layout().setSpacing(self.titleEdgeOffset)
        self.TitleBar.setObjectName("TitleBar")
        self.MainLayout.addWidget(self.TitleBar, 0, 0, 1, 2)

        # Creates title and icon
        self.Logo = QLabel()
        self.logoPixmap = QPixmap("Assets/Icons/Logo.png")
        self.logoPixmap = self.logoPixmap.scaledToHeight(self.TitleBar.height() - self.titleEdgeOffset * 2)
        self.Logo.setFixedSize(self.TitleBar.height(), self.TitleBar.height())
        self.Logo.setPixmap(self.logoPixmap)
        self.TitleBar.layout().addWidget(self.Logo)

        self.Title = QLabel("Macro Ultimate")
        self.Title.setFont(QFont("Sublima ExtraBold", 10))
        self.Title.setObjectName("Title")
        self.TitleBar.layout().addWidget(self.Title)

        self.TitleBar.layout().insertSpacing(2, self.screenSize.width())

        # Creates custom titlebar buttons
        self.MinimizeButton = QTitleButton(self.TitleBar, "Assets/Icons/minimize.svg")
        self.MinimizeButton.disable()
        self.MinimizeButton.setObjectName("MinimizeButton")
        self.MinimizeButton.mousePressEvent = self.minimize

        self.ExitButton = QTitleButton(self.TitleBar, "Assets/Icons/exit.svg")
        self.ExitButton.disable()
        self.ExitButton.setObjectName("ExitButton")
        self.ExitButton.mousePressEvent = self.exit

        # Sets up container for command nodes
        self.NodeBox = QWidget(self.centralWidget())
        self.NodeBox.setObjectName("NodeBox")
        self.NodeBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.NodeBox.setFixedWidth(self.width() // 3)
        self.NodeBox.setLayout(QVBoxLayout())

        self.MainLayout.addWidget(self.NodeBox, 1, 0, 1, 1)

        # Sets up container for command nodes' properties
        self.PropertyContainer = QWidget(self.centralWidget())
        self.PropertyContainer.setObjectName("PropertyContainer")
        self.PropertyContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.PropertyContainer.setLayout(QVBoxLayout())
        self.PropertyContainer.layout().setContentsMargins(10, 0, 10, 10)

        # Sets up property section elements
        self.PropertyTitle = QLabel("Properties")
        self.PropertyTitle.setFont(self.PropertyFont)
        self.PropertyTitle.setObjectName("PropertyTitle")
        self.PropertyContainer.layout().addWidget(self.PropertyTitle)

        self.PropertyBox = QWidget(self.centralWidget())
        self.PropertyBox.setObjectName("PropertyBox")
        self.PropertyBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.PropertyBox.setLayout(QVBoxLayout())
        self.PropertyContainer.layout().addWidget(self.PropertyBox)

        self.MainLayout.addWidget(self.PropertyContainer, 1, 1, 1, 1)

    def exit(self, event):
        app.quit()

    def minimize(self, event):
        self.setWindowState(Qt.WindowState.WindowMinimized)

    def showEvent(self, a0) -> None:
        self.activateWindow()
        self.setFocus()
        self.setWindowState(Qt.WindowState.WindowActive)
        self.raise_()

        self.centralWidget().activateWindow()

        print(self.isActiveWindow())



def main():
    window = MainWindow()
    window.setWindowTitle('AutoClicker Ultimate')

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()