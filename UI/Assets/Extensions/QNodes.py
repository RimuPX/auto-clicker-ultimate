from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QSizePolicy, QScrollArea, QHBoxLayout

from UI.Assets.Extensions.HelpfulFuncs import setShadow
from UI.Assets.Extensions.QProperties import QPropertyBox
from UI.Assets.Extensions.Singleton import *
from UI.Assets.StyleSheets import MainSheet


class QActionPanel(Singleton, QLabel):

    def __init__(self):
        super(QLabel, self).__init__()

        self.setLayout(QHBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setObjectName("NodeActionPanel")
        self.setStyleSheet(MainSheet.Sheet)
        self.layout().setContentsMargins(0, 0, 10, 5)
        self.setFixedSize(QNodeBox.getInstance().width(), 30)

class QActionButton(QLabel):

    def __init__(self, sign: str, pressAction): #specify function type
        self.pressAction = pressAction
        super(QLabel, self).__init__(sign)

        self.setFont(QFont(MainSheet.propertyFont.family(), 13))

    def mousePressEvent(self, event):
        try:
            self.pressAction()
            super(QLabel, self).mouseMoveEvent(event)
        except Exception as e:
            print(e)

class QNode(QLabel):

    def __init__(self):
        self.NodeBox = QNodeBox.getInstance()

        super(QLabel, self).__init__("Empty")
        self.setObjectName("Node")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(self.NodeBox.nodeHeight)
        self.setStyleSheet(MainSheet.Sheet)
        self.setFont(QFont(MainSheet.propertyFont.family(), 14))
        self.setContentsMargins(5, 0, 0, 4)

        self.NodeBox.NodeList.layout().addWidget(self)

        self.properties = {"Action: ": "Space", "Hold for: ": 3}

    def mousePressEvent(self, event):
        controlDown = self.window().controlDown
        shiftDown = self.window().shiftDown

        if controlDown:
            if not self in self.NodeBox.selectedNodes:
                self.NodeBox.selectNodes([self])
            elif not shiftDown:
                self.NodeBox.deselectNodes([self])
        else:
            self.NodeBox.deselectNodes(self.NodeBox.selectedNodes)
            self.NodeBox.selectNodes([self])

        if shiftDown:
            self.NodeBox.selectRange(self.NodeBox.NodeList.layout().indexOf(self), self.NodeBox.NodeList.layout().indexOf(self.NodeBox.lastSelectedNode))
        else:
            self.NodeBox.lastSelectedNode = self

        QPropertyBox.getInstance().displayNode(self)
        self.window().mousePressEvent(event)

    def delete(self):
        self.NodeBox.NodeList.layout().removeWidget(self)
        self.deleteLater()


class QLoop(Singleton, QNode):

    def __init__(self):
        self.NodeBox = QNodeBox.getInstance()

        super(QNode, self).__init__()
        super(Singleton, self).__init__()

        self.setFont(QFont(MainSheet.propertyFont.family(), 18))
        self.setText('Loop')
        self.setFixedHeight(round(self.NodeBox.nodeHeight * 1.5))
        self.setContentsMargins(3, 0, 0, 4)

        self.NodeBox.lastSelectedNode = self


class QNodeBox(Singleton, QLabel):

    def __init__(self):
        super(QLabel, self).__init__()

        self.selectedNodes = []
        self.lastSelectedNode = None
        self.nodeHeight = self.height() // 16

        # Constructs node box
        self.setObjectName("Box")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(self.width() // 3)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        setShadow(self)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Sets up node parameteres
        QNodeBox.nodeHeight = self.geometry().height() // 18

        self.NodeList = QLabel(self)
        self.NodeList.setLayout(QVBoxLayout())
        self.NodeList.layout().setContentsMargins(0, 0, 0, 0)
        self.NodeList.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        for i in range(0, 50): self.addNode()

        self.NodeScroll = QScrollArea()
        self.NodeScroll.setWidget(self.NodeList)
        self.NodeScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.AddButton = QActionButton("+", self.addNode)
        self.RemoveButton = QActionButton("-", self.deleteNodes)

        self.NodeActionPanel = QActionPanel()
        self.NodeActionPanel.layout().addWidget(self.AddButton)
        self.NodeActionPanel.layout().addWidget(self.RemoveButton)
        self.layout().addWidget(self.NodeActionPanel)

        # Sets cell proportions
        self.layout().setStretch(0, 3)
        self.layout().setStretch(1, 12)
        self.layout().setStretch(2, 1)

        # Sets spacings
        self.spacing = 0
        self.layout().setSpacing(self.spacing)
        self.NodeList.layout().setSpacing(self.spacing)

        # Creates essential widgets
        self.Loop = QLoop()

        # Adds widgets to layout
        self.layout().addWidget(self.Loop, 0)
        self.layout().addWidget(self.NodeList, 1)
        self.layout().addWidget(self.NodeActionPanel, 2)

    def selectNodes(self, nodes):
        for node in nodes:
            node.setObjectName("SelectedNode")
            node.setStyleSheet(MainSheet.Sheet)
            if not node in self.selectedNodes: self.selectedNodes.append(node)

    def deselectNodes(self, nodes):
        selectedNodeBuffer = []
        for node in self.selectedNodes:
            if not node in nodes:
                selectedNodeBuffer.append(node)
            else:
                node.setObjectName("Node")
                node.setStyleSheet(MainSheet.Sheet)
        self.selectedNodes = selectedNodeBuffer

    def selectRange(self, p1: int, p2: int):
        pStart = min(p1, p2)
        pEnd = max(p1, p2)

        if pStart == -1:
            self.selectNodes([self.Loop])
            pStart = max(0, pStart)

        for i in range(pStart, pEnd + 1):
            self.selectNodes([QNodeBox.getInstance().NodeList.layout().itemAt(i).widget()])

    def addNode(self):
        node = QNode()
        self.NodeList.layout().addWidget(node)

    def deleteNodes(self):
        for node in self.selectedNodes:
            node.delete()
        self.selectedNodes = []

    def mousePressEvent(self, event):
        self.deselectNodes(self.selectedNodes)
        self.window().mousePressEvent(event)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_A and self.window().controlDown:
            nodes = [QLoop.getInstance()]
            for nodeIndex in range(0, self.NodeList.layout().count()):
                nodes.append(self.NodeList.layout().itemAt(nodeIndex).widget())
            self.selectNodes(nodes)
        self.window().keyPressEvent(event)