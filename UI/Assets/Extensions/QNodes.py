from PyQt6.QtWidgets import QLabel, QVBoxLayout, QSizePolicy, QWidget, QBoxLayout

from UI.Assets.Extensions.QProperties import *
from UI.Assets.Extensions.Singleton import *

class QActionPanel(Singleton, QLabel):

    def __init__(self, parentHeight: int):
        super(QLabel, self).__init__()

        self.scaleFactor = 8

        self.setObjectName("Box")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(parentHeight)
        setShadow(self)

class QActionButton(QLabel):

    def __init__(self, sign: str, pressAction): #specify function type
        self.pressAction = pressAction
        # super(QActionButton, self).__init__(sign)
        super(QLabel, self).__init__(sign)

        self.setObjectName("SelectedNode")

        self.setFont(
            QFont(MainSheet.propertyFont.family(), 13)
        )

    def mousePressEvent(self, event):
        print('pressed')
        try:
            self.pressAction()
            super(QLabel, self).mouseMoveEvent(event)
        except Exception as e:
            print(e)

class QNode(QLabel):

    def __init__(self, name: str, height: int, parent: QWidget):
        super(QLabel, self).__init__(name)
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
            QNodeBox.selectRange(QNodeBox.getInstance().NodeList.layout().indexOf(self), QNodeBox.getInstance().NodeList.layout().indexOf(QNodeBox.lastSelectedNode))
        else:
            QNodeBox.lastSelectedNode = self

    def delete(self):
        self.parent().layout().removeWidget(self)
        self.deleteLater()


class QLoop(QNode, Singleton):

    def __init__(self, parent):
        super(Singleton, self).__init__("Loop", int(MainSheet.propertyFont.pointSize() * 2.2), parent)
        self.setFont(QFont(MainSheet.propertyFont.family(), 18))
        QNodeBox.lastSelectedNode = self


class QNodeBox(Singleton, QLabel):

    selectedNodes = []
    lastSelectedNode = None

    nodeHeight = 0

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
            QNodeBox.selectNodes([QLoop(QNodeBox.getInstance())])
            pStart = max(0, pStart)

        for i in range(pStart, pEnd + 1):
            QNodeBox.selectNodes([QNodeBox.getInstance().NodeList.layout().itemAt(i).widget()])

    def addNode(self):
        node = QNode("Empty", QNodeBox.getInstance().nodeHeight, QNodeBox.getInstance().NodeList)
        self.NodeList.layout().addWidget(node)

    def deleteNodes(self):
        pass

    def __init__(self):
        super(QLabel, self).__init__()

        # Constructs node box
        self.setObjectName("Box")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(self.width() // 3)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        setShadow(self)

        # Sets up node parameteres
        QNodeBox.nodeHeight = self.geometry().height() // 18

        self.NodeList = QWidget(self)
        self.NodeList.setLayout(QVBoxLayout())
        self.NodeList.layout().setContentsMargins(0, 0, 0, 0)
        self.NodeList.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.NodeActionPanel = QWidget(self)
        self.NodeActionPanel.setLayout(QHBoxLayout())
        self.NodeActionPanel.layout().setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.NodeActionPanel.setObjectName("NodeActionPanel")
        self.NodeActionPanel.layout().setContentsMargins(0, 0, 5, 5)
        self.NodeActionPanel.setFixedHeight(50)

        self.AddButton = QActionButton("+", self.addNode)
        self.RemoveButton = QActionButton("-", self.deleteNodes)

        self.NodeActionPanel.layout().addWidget(self.AddButton)
        self.NodeActionPanel.layout().addWidget(self.RemoveButton)


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

        # Adds widgets to layout
        self.layout().addWidget(self.Loop, 0)
        self.layout().addWidget(self.NodeList, 1)
        self.layout().addWidget(self.NodeActionPanel, 2)
