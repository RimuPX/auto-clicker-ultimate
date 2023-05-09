from PyQt6.QtCore import Qt, QPoint, QEvent
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QSizePolicy, QScrollArea, QHBoxLayout

from Assets.Extensions.HelpfulFuncs import setShadow, boxesOverlap
from Assets.Extensions.QProperties import QPropertyBox
from Assets.Extensions.Singleton import *
from Assets.StyleSheets import MainSheet


class QActionPanel(Singleton, QLabel):

    def __init__(self):
        super(QLabel, self).__init__()

        self.setLayout(QHBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setObjectName("NodeActionPanel")
        self.setStyleSheet(MainSheet.Sheet)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.setFixedSize(QNodeBox.getInstance().width(), 30)

class QActionButton(QLabel):

    def __init__(self, sign: str, pressAction):
        self.pressAction = pressAction
        super(QLabel, self).__init__(sign)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(15)

        self.setFont(QFont(MainSheet.propertyFont.family(), 13))

    def mousePressEvent(self, event):
        try:
            self.pressAction()
            self.window().mousePressEvent(event)
        except Exception as e:
            print(e)

class QNode(QLabel):

    def __init__(self):
        self.NodeBox = QNodeBox.getInstance()

        super(QLabel, self).__init__(str(QNodeBox.getInstance().NodeList.layout().count()))
        self.setObjectName("Node")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(self.NodeBox.nodeHeight)
        self.setStyleSheet(MainSheet.Sheet)
        self.setFont(QFont(MainSheet.propertyFont.family(), 14))
        self.setContentsMargins(5, 0, 0, 4)

        self.shiftDown = False
        self.controlDown = False
        self.selected = False

        self.properties = {"Action: ": "Space", "Hold for: ": 3}

    def mousePressEvent(self, event):
        self.shiftDown = self.window().shiftDown
        self.controlDown = self.window().controlDown
        self.selected = self in self.NodeBox.selectedNodes

        self.NodeBox.clickedOnSelectedNode = self.selected
        self.NodeBox.clickedOnNode = True

        if self.controlDown:
            if not self in self.NodeBox.selectedNodes:
                self.NodeBox.selectNodes([self])

        if self.shiftDown:
            if not self.controlDown:
                self.NodeBox.deselectNodes(self.NodeBox.selectedNodes)
            self.NodeBox.selectRange(self.NodeBox.NodeList.layout().indexOf(self), self.NodeBox.NodeList.layout().indexOf(self.NodeBox.lastSelectedNode))
        else:
            self.NodeBox.lastSelectedNode = self

        if not self.controlDown and not self.shiftDown and not self.selected:
            self.NodeBox.deselectNodes(self.NodeBox.selectedNodes)
            self.NodeBox.selectNodes([self])

        #QPropertyBox.getInstance().displayNode(self)

        self.window().mousePressEvent(event)

    def mouseReleaseEvent(self, event):

        releasedInBounds = boxesOverlap(event.pos(), event.pos(), self.pos(), QPoint(self.pos().y() + self.width(), self.pos().y() + self.height()))

        if self.controlDown\
                and not self.shiftDown\
                and self.selected:
            self.NodeBox.deselectNodes([self])

        if not self.controlDown and not self.shiftDown and releasedInBounds:
            self.NodeBox.deselectNodes(self.NodeBox.selectedNodes)
            self.NodeBox.selectNodes([self])

        self.selected = self in self.NodeBox.selectedNodes
        self.window().mouseReleaseEvent(event)

    def delete(self):
        self.NodeBox.deselectNodes([self])
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

    def delete(self):
        pass


class QNodeBox(Singleton, QLabel):

    def __init__(self):
        super(QLabel, self).__init__()

        # Adds node box attributes
        self.selectedNodes = []
        self.lastSelectedNode = None
        self.nodeHeight = self.height() // 16
        self.clickedOnSelectedNode = False
        self.clickedOnNode = True

        # Constructs node box
        self.setObjectName("Box")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(self.width() // 3)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        setShadow(self)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        # Sets up node parameteres
        QNodeBox.nodeHeight = self.geometry().height() // 18

        self.NodeList = QWidget(self)
        self.NodeList.setLayout(QVBoxLayout())
        self.NodeList.layout().setContentsMargins(0, 0, 0, 0)
        self.NodeList.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.NodeScroll = QScrollArea()
        self.NodeScroll.setObjectName("NodeScroll")
        self.NodeScroll.setWidget(self.NodeList)
        self.NodeScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.NodeScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.NodeScroll.setWidgetResizable(True)

        self.AddButton = QActionButton("+", self.addNode)
        self.RemoveButton = QActionButton("-", self.deleteNodes)

        self.NodeActionPanel = QActionPanel()
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

        # Creates essential widgets
        self.Loop = QLoop()

        # Adds widgets to layout
        self.layout().addWidget(self.Loop)
        self.layout().addWidget(self.NodeScroll)
        self.layout().addWidget(self.NodeActionPanel)

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
        if not self.selectedNodes and self.NodeList.layout().count() > 0:
            node = self.NodeList.layout().itemAt(self.NodeList.layout().count() - 1).widget()
            node.delete()
        else:
            for node in self.selectedNodes:
                node.delete()

    def moveNodes(self, rawMousePressPos: QPoint, rawMouseHoldPos: QPoint):
        try:
            mousePressPos = self.NodeList.mapFrom(self, rawMousePressPos)
            mouseHoldPos = self.NodeList.mapFrom(self, rawMouseHoldPos)
        except Exception as e:
            print(e)

    def mouseSelect(self, mousePressPos: QPoint, mouseHoldPos: QPoint):
        legacySelectedNodes = self.selectedNodes

        nodes = []
        for nodeIndex in range(0, self.NodeList.layout().count()):
            nodes.append(self.NodeList.layout().itemAt(nodeIndex).widget())
        for node in nodes:
            absNodePos = self.NodeList.mapTo(self, QPoint(node.x(), node.y()))
            if boxesOverlap(mousePressPos,
                            mouseHoldPos,
                            absNodePos,
                            QPoint(absNodePos.x() + node.width(), absNodePos.y() + node.height())):
                self.selectNodes([node])
                if node not in legacySelectedNodes: self.lastSelectedNode = node
            else:
                self.deselectNodes([node])

        loop = self.Loop
        absLoopPos = QPoint(loop.x(), loop.y())
        if boxesOverlap(mousePressPos,
                        mouseHoldPos,
                        absLoopPos,
                        QPoint(absLoopPos.x() + loop.width(), absLoopPos.y() + loop.height())):
            self.selectNodes([loop])
            if loop not in legacySelectedNodes: self.lastSelectedNode = node
            self.lastSelectedNode = loop
        else:
            self.deselectNodes([loop])

    def eventFilter(self, source, event: QEvent):
        if event.type() == QEvent.Type.MouseButtonPress and source == self.window():
            if not self.clickedOnNode: self.deselectNodes(self.selectedNodes)
            self.clickedOnNode = False
            self.window().mousePressPos = event.pos()
        if event.type() == QEvent.Type.MouseMove and source == self.window():
            mouseHoldPos = event.pos()
            mousePressPos = self.mapFrom(self.window(), self.window().mousePressPos)
            self.mouseSelect(mousePressPos, mouseHoldPos)
        if event.type() == QEvent.Type.MouseButtonRelease and source == self.window():
            self.clickedOnSelectedNode = False
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_A and self.window().controlDown:
            nodes = [self.Loop]
            for nodeIndex in range(0, self.NodeList.layout().count()):
                nodes.append(self.NodeList.layout().itemAt(nodeIndex).widget())
            self.selectNodes(nodes)
        if event.key() == Qt.Key.Key_Delete:
            self.deleteNodes()
        self.window().keyPressEvent(event)