from PyQt6.QtCore import Qt

from Assets.Extensions.HelpfulFuncs import *
from Assets.StyleSheets import *
from Assets.Extensions.Singleton import *

class QPropertyBox(QLabel, Singleton):
    def __init__(self):
        super(QPropertyBox, self).__init__()

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