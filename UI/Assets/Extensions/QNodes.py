from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from HelpfulFuncs import *

m()

propertyFont = QFont("Sublima ExtraBold", 18)
MainSheet = ""

class QActionPanel(QLabel):
    def __init__(self, parent: QWidget):
        super(QActionPanel, self).__init__(parent)

        self.actionPanelScaleFactor = 8

        self.setObjectName("Box")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        #self.setFixedWidth(200)
        self.setFixedHeight(parent.height() // self.actionPanelScaleFactor)
        parent.layout().addWidget(self, 1, 0, 1, 1)
        parent.layout().setRowStretch(1, 1)

class QActionButton(QLabel):
    def __init__(self, sign: str, font: QFont):
        super(QActionButton, self).__init__(sign)
        self.font = QFont(font.family(), 13)
        self.setFont(self.font)


class QNode(QLabel):
    selectedNodes = {}

    def __init__(self, name: str, height: int, font: QFont):
        super(QNode, self).__init__(name)
        self.setObjectName("Node")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(height)
        self.setStyleSheet(MainSheet)
        self.setFont(font)
        self.setContentsMargins(5, 0, 0, 4)

        self.Properties = {"Action: ": "Space", "Hold for: ": 12}

    def mousePressEvent(self, event) -> None:
        self.setObjectName("SelectedNode")
        self.setStyleSheet(MainSheet)

    def delete(self):
        self.parent().layout().removeWidget(self)
        self.deleteLater()

class QNodeBox(QLabel):
    def __init__(self, styleSheet: str):
        super(QNodeBox, self).__init__()

        MainSheet = styleSheet

        # Constructs node box
        self.setObjectName("Box")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(self.width() // 3)
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(8, 8, 8, 8)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.nodeHeight = self.geometry().height() // 18
        self.nodeFont = QFont("Sublima ExtraBold", 14)

        self.NodeList = QWidget(self)
        self.NodeList.setLayout(QVBoxLayout())
        self.NodeList.layout().setContentsMargins(0, 0, 0, 0)
        self.NodeList.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout().addWidget(self.NodeList, 1, 0, 1, 2)

        self.NodeActionPanel = QWidget(self)
        self.NodeActionPanel.setLayout(QHBoxLayout())
        self.NodeActionPanel.layout().setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.NodeActionPanel.setObjectName("NodeActionPanel")
        self.NodeActionPanel.layout().setContentsMargins(0, 0, 0, 0)
        self.NodeActionPanel.setFixedHeight(20)

        self.AddButton = QActionButton("+", self.nodeFont)
        self.RemoveButton = QActionButton("-", self.nodeFont)

        self.NodeActionPanel.layout().addWidget(self.RemoveButton)
        self.NodeActionPanel.layout().addWidget(self.AddButton)

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

        # Creates essential widgets
        self.Loop = QNode("Loop", self.nodeHeight * 4 // 3, propertyFont)
        self.layout().addWidget(self.Loop, 0, 0, 1, 2)
        self.addNode("Alt + F")
        self.addNode("X")

    def addNode(self, name: str):
        node = QNode(name, self.nodeHeight, self.nodeFont)
        self.NodeList.layout().addWidget(node)