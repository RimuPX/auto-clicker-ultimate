from PyQt6.QtCore import Qt

from Assets.Extensions.HelpfulFuncs import *
from Assets.StyleSheets import *
from Assets.Extensions.Singleton import *
from PyQt6.QtWidgets import QLabel, QSizePolicy, QGridLayout

class QProperty(QLabel):
    def __init__(self, key: str):
        super(QProperty, self).__init__(key)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedSize(120, 22)
        self.setStyleSheet(MainSheet.Sheet)
        self.setFont(QFont(MainSheet.propertyFont.family(), 14))
        self.setContentsMargins(2, 0, 0, 4)

class QPropertyBox(Singleton, QLabel):

    def __init__(self):
        super(QLabel, self).__init__()

        # Initializes the box
        self.setObjectName("Box")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setLayout(QGridLayout())

        # Creates layout
        self.layout().setContentsMargins(10, 0, 10, 10)
        self.layout().setSpacing(10)
        self.layout().setColumnStretch(0, 1)
        self.layout().setColumnStretch(1, 2)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        setShadow(self)

        # Sets up property section elements
        self.PropertyTitle = QLabel("Properties")
        self.PropertyTitle.setFont(MainSheet.propertyFont)
        self.PropertyTitle.setObjectName("PropertyTitle")
        self.layout().addWidget(self.PropertyTitle, 0, 0, 1, 2)

    def displayNode(self, node):
        properties = node.properties

        for key in properties.keys():
            label = QProperty(key)

            self.layout().addWidget(label)