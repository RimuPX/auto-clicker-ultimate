from PyQt6.QtCore import Qt

from Assets.Extensions.HelpfulFuncs import *
from Assets.StyleSheets import *

class QActionPanel(QLabel):

    __instance = None
    hasInstance = False

    def __new__(cls, *args):
        if not cls.__instance:
            cls.__instance = super(QActionPanel, cls).__new__(cls)
        return cls.__instance

    def __init__(self, parent: QWidget):
        if QActionPanel.hasInstance: return

        super(QActionPanel, self).__init__(parent)

        self.scaleFactor = 8

        self.setObjectName("Box")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(parent.height())
        setShadow(self)

        QActionPanel.hasInstance = True

class QActionButton(QLabel):
    def __init__(self, sign: str):
        super(QActionButton, self).__init__(sign)
        self.setFont(QFont(MainSheet.propertyFont.family(), 13))

class QNode(QLabel):

    def __init__(self, name: str, height: int, parent: QWidget):
        super(QNode, self).__init__(name)
        self.setObjectName("Node")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(height)
        self.setStyleSheet(MainSheet.Sheet)
        self.setFont(QFont(MainSheet.propertyFont.family(), 14))
        self.setContentsMargins(5, 0, 0, 4)

        parent.layout().addWidget(self)

        self.Properties = {"Action: ": "Space", "Hold for: ": 12}


    def mousePressEvent(self, event):
        controlDown = self.window().controlDown
        shiftDown = self.window().shiftDown

        if controlDown:
            if not self in QNodeBox.selectedNodes:
                QNodeBox.selectNodes([self])
            elif not shiftDown:
                QNodeBox.deselectNodes([self])
        else:
            QNodeBox.deselectNodes(QNodeBox.selectedNodes)
            QNodeBox.selectNodes([self])

        if shiftDown:
            print('Layout: ', QNodeBox().NodeList.layout().indexOf(QNodeBox.lastSelectedNode))
            QNodeBox.selectRange(QNodeBox().NodeList.layout().indexOf(self), QNodeBox().NodeList.layout().indexOf(QNodeBox.lastSelectedNode)) # fix
        else:
            QNodeBox.lastSelectedNode = self

    def delete(self):
        self.parent().layout().removeWidget(self)
        self.deleteLater()

class QLoop(QNode):

    __instance = None
    hasInstance = False

    def __new__(cls, *args):
        if not cls.__instance:
            cls.__instance = super(QLoop, cls).__new__(cls)
        return cls.__instance

    def __init__(self, parent):
        if QLoop.hasInstance: return

        super(QLoop, self).__init__("Loop", int(MainSheet.propertyFont.pointSize() * 2.2), parent)
        self.setFont(QFont(MainSheet.propertyFont.family(), 18))
        QNode.lastSelectedNode = self

        QLoop.hasInstance = True

class QNodeBox(QLabel):

    selectedNodes = []
    lastSelectedNode = None

    __instance = None
    hasInstance = False

    @staticmethod
    def selectNodes(nodes):
        for node in nodes:
            node.setObjectName("SelectedNode")
            node.setStyleSheet(MainSheet.Sheet)
            if not node in QNodeBox.selectedNodes: QNodeBox.selectedNodes.append(node)

    @staticmethod
    def deselectNodes(nodes):
        selectedNodeBuffer = []
        for node in QNodeBox.selectedNodes:
            if not node in nodes:
                selectedNodeBuffer.append(node)
            else:
                node.setObjectName("Node")
                node.setStyleSheet(MainSheet.Sheet)
        QNodeBox.selectedNodes = selectedNodeBuffer

    @staticmethod
    def selectRange(p1: int, p2: int):
        pStart = min(p1, p2)
        pEnd = max(p1, p2)

        if pStart == -1:
            QNodeBox.selectNodes([QLoop(QNodeBox())])
            pStart = max(0, pStart)

        for i in range(pStart, pEnd + 1):
            QNodeBox.selectNodes([QNodeBox().NodeList.layout().itemAt(i).widget()])
            print(pStart, ' ', pEnd)

    def addNode(self, name: str):
        node = QNode(name, self.nodeHeight, self.NodeList)
        self.NodeList.layout().addWidget(node)

    def deleteNodes(self):
        pass

    def __new__(cls, *args):
        if not cls.__instance:
            cls.__instance = super(QNodeBox, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if QNodeBox.hasInstance: return

        super(QNodeBox, self).__init__()

        # Constructs node box
        self.setObjectName("Box")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(self.width() // 3)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        setShadow(self)

        # Sets up node parameteres
        self.nodeHeight = self.geometry().height() // 18

        self.NodeList = QWidget(self)
        self.NodeList.setLayout(QVBoxLayout())
        self.NodeList.layout().setContentsMargins(0, 0, 0, 0)
        self.NodeList.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.NodeActionPanel = QWidget(self)
        self.NodeActionPanel.setLayout(QHBoxLayout())
        self.NodeActionPanel.layout().setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.NodeActionPanel.setObjectName("NodeActionPanel")
        self.NodeActionPanel.layout().setContentsMargins(0, 0, 0, 0)
        self.NodeActionPanel.setFixedHeight(20)

        self.AddButton = QActionButton("+")
        self.RemoveButton = QActionButton("-")

        self.NodeActionPanel.layout().addWidget(self.RemoveButton)
        self.NodeActionPanel.layout().addWidget(self.AddButton)

        # Sets cell proportions
        self.layout().setStretch(0, 3)
        self.layout().setStretch(1, 12)
        self.layout().setStretch(2, 1)

        # Sets spacings
        self.spacing = 0
        self.layout().setSpacing(self.spacing)
        self.NodeList.layout().setSpacing(self.spacing)
        QNode.NodeLayout = self.NodeList.layout()


        # Creates essential widgets
        self.Loop = QLoop(self)
        self.addNode("Alt + F")
        self.addNode("X")
        self.addNode("F")
        self.addNode("M")

        # Adds widgets to layout
        self.layout().addWidget(self.Loop, 0)
        self.layout().addWidget(self.NodeList, 1)
        self.layout().addWidget(self.NodeActionPanel, 2)

        QNodeBox.hasInstance = True

    def mousePressEvent(self, event):
        QNodeBox.deselectNodes(QNodeBox.selectedNodes)
        super().mousePressEvent(event)