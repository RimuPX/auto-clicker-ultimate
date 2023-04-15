import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap, QColor
from Assets import StyleSheets

app = QApplication(sys.argv)

def setShadow(widget: QWidget):
    ShadowEffect = QGraphicsDropShadowEffect()
    ShadowEffect.setBlurRadius(25)
    ShadowEffect.setColor(QColor(19, 50, 158, 100))
    ShadowEffect.setOffset(0, 3)

    widget.setGraphicsEffect(ShadowEffect)

def recolorPixmap(pixmap: QPixmap, color: QColor):
    tmpImage = pixmap.toImage()

    for x in range(tmpImage.width()):
        for y in range(tmpImage.height()):
            tmpImage.setPixelColor(x, y, QColor(color.red(), color.green(), color.blue(), tmpImage.pixelColor(x, y).alpha()))

    return QPixmap.fromImage(tmpImage)

class QPropertyBox(QLabel):
    def __init__(self):
        super(QPropertyBox, self).__init__()
        self.setObjectName("PropertyBox")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setLayout(QVBoxLayout())

    def ShowProperties(self):
        n=0

class QNode(QLabel):
    selectedNodes = {}

    def __init__(self, name: str, height: int, font: QFont):
        super(QNode, self).__init__(name)
        self.setObjectName("Node")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(height)
        self.setStyleSheet(StyleSheets.MainSheet)
        self.setFont(font)
        self.setContentsMargins(5, 0, 0, 4)

        self.Properties = {"Action: ": "Space", "Hold for: ": 12}

    def mousePressEvent(self, event) -> None:
        self.setObjectName("SelectedNode")
        self.setStyleSheet(StyleSheets.MainSheet)

    def delete(self):
        self.parent().layout().removeWidget(self)
        self.deleteLater()

class QNodeBox(QLabel):
    def __init__(self, propertyFont: QFont):
        super(QNodeBox, self).__init__()

        # Constructs node box
        self.setObjectName("NodeBox")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(self.width() // 3)
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(8, 8, 8, 8)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.nodeHeight = self.geometry().height() // 18
        self.nodeFont = QFont("Sublima ExtraBold", 14)

        # Creates essential widgets
        self.Loop = QNode("Loop", self.nodeHeight * 4 // 3, propertyFont)
        self.layout().addWidget(self.Loop, 0, 0, 1, 2)

        self.NodeList = QWidget(self)
        self.NodeList.setLayout(QVBoxLayout())
        self.NodeList.layout().setContentsMargins(0, 0, 0, 0)
        self.NodeList.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout().addWidget(self.NodeList, 1, 1, 1, 1)

        self.NodeActionPanel = QWidget(self)
        self.NodeActionPanel.setObjectName("Node")

        self.layout().addWidget(self.NodeActionPanel, 2, 0, 1, 2)

        # Sets spacings
        self.spacing = 6
        self.layout().setSpacing(self.spacing)
        self.NodeList.layout().setSpacing(self.spacing)

        # Sets cell proportions
        self.layout().setRowStretch(0, 3)
        self.layout().setRowStretch(1, 12)
        self.layout().setRowStretch(2, 1)
        self.layout().setColumnStretch(0, 1)
        self.layout().setColumnStretch(1, 16)

    def addNode(self):
        node = QNode("Loop", self.nodeHeight, self.nodeFont)
        self.NodeList.layout().addWidget(node)

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # Adds font to database
        QFontDatabase.addApplicationFont("Assets/Fonts/Sublima-ExtraBold.otf")
        self.propertyFont = QFont("Sublima ExtraBold", 18)

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
        self.NodeBox = QNodeBox(self.propertyFont)
        self.NodeBox.addNode()
        self.NodeBox.addNode()

        self.MainLayout.setRowStretch(0, 7)
        self.MainLayout.addWidget(self.NodeBox, 0, 0, 1, 1)

        # Creates a panel with context buttons
        self.actionPanelScaleFactor = 8

        self.ActionPanel = QWidget(self.centralWidget())
        self.ActionPanel.setObjectName("NodeBox")
        self.ActionPanel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ActionPanel.setFixedWidth(self.NodeBox.width())
        self.ActionPanel.setFixedHeight(self.height() // self.actionPanelScaleFactor)
        self.MainLayout.addWidget(self.ActionPanel, 1, 0, 1, 1)
        self.MainLayout.setRowStretch(1, 1)

        # Sets up container for command nodes' properties
        self.PropertyBox = QPropertyBox()
        self.MainLayout.addWidget(self.PropertyBox)
        self.PropertyBox.setObjectName("PropertyBox")
        self.PropertyBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.PropertyBox.setLayout(QVBoxLayout())
        self.PropertyBox.layout().setContentsMargins(10, 0, 10, 10)
        self.PropertyBox.layout().setSpacing(10)
        self.PropertyBox.layout().setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Sets up property section elements
        self.PropertyTitle = QLabel("Properties")
        self.PropertyTitle.setFont(self.propertyFont)
        self.PropertyTitle.setObjectName("PropertyTitle")
        self.PropertyBox.layout().addWidget(self.PropertyTitle)

        self.MainLayout.addWidget(self.PropertyBox, 0, 1, self.MainLayout.rowCount() - 1, 1)


        setShadow(self.ActionPanel)
        setShadow(self.NodeBox)
        setShadow(self.PropertyBox)

    def exit(self, event):
        app.quit()

    def minimize(self, event):
        self.showMinimized()

    def showEvent(self, a0) -> None:
        self.activateWindow()
        self.setFocus()
        self.setWindowState(Qt.WindowState.WindowActive)
        self.raise_()

        self.centralWidget().activateWindow()



def main():
    window = MainWindow()
    window.setWindowTitle('AutoClicker Ultimate')

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()