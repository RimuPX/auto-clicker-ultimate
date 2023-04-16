import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont



propertyFont = QFont("Sublima ExtraBold", 18)

class QPropertyBox(QLabel):
    def __init__(self):
        super(QPropertyBox, self).__init__()

        setShadow(self)

        self.setObjectName("Box")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(10, 0, 10, 10)
        self.layout().setSpacing(10)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Sets up property section elements
        self.PropertyTitle = QLabel("Properties")
        self.PropertyTitle.setFont(propertyFont)
        self.PropertyTitle.setObjectName("PropertyTitle")
        self.layout().addWidget(self.PropertyTitle)

    def ShowProperties(self):
        n=0