from PyQt6.QtGui import QColor

titlebarImageColor = QColor(74, 74, 103)
titleBarSelectedImageColor = QColor(255, 255, 255)

MainSheet = """

QWidget#CentralWidget {
background-color: rgb(32, 32, 42);
}



QWidget#TitleBar {
background-color: rgb(38, 38, 50);
}

QWidget#ExitButton {
background-color: transparent;
}
QWidget::hover#ExitButton {
background-color: rgb(255, 38, 50);
}

QWidget#MinimizeButton {
background-color: transparent;
}
QWidget::hover#MinimizeButton {
background-color: rgb(74, 74, 103);
}

QWidget#Title {
color: rgb(74, 74, 103);
}



QWidget#NodeBox {
background-color: rgb(35, 35, 47);
}

QWidget#PropertyBox {
background-color: rgb(35, 35, 47);
border-radius: 5;
}
QWidget#PropertyTitle {
color: rgb(255, 255, 255);
}

"""


titleBar = """
background-color: rgb(38, 38, 50);
"""

lightBox = """
background-color: rgb(35, 35, 47);
"""

darkBox = """
background-color: rgb(32, 32, 42);
"""

lightText = """
color: rgb(74, 74, 103);
"""

titleText = """
color: rgb(255, 255, 255);
"""

roundedParam = """
border-radius: 5;
"""