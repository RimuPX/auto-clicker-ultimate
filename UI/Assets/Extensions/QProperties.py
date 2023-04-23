from PyQt6.QtCore import Qt

from Assets.Extensions.HelpfulFuncs import *
from Assets.StyleSheets import *

class QPropertyBox(QLabel):

    __instance = None
    hasInstance = False

    def __new__(cls, *args):
        if not cls.__instance:
            cls.__instance = super(QPropertyBox, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if QPropertyBox.hasInstance: return

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

        QPropertyBox.hasInstance = True