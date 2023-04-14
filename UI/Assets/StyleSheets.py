from PyQt6.QtGui import QColor

titlebarImageColor = QColor(74, 74, 103)
titleBarSelectedImageColor = QColor(255, 255, 255)

BackgroundColor = "rgb(32, 32, 42);"
TitleBarColor = "rgb(38, 38, 50)"
ExitButtonColor = "rgb(255, 38, 50)"
MidColor = "rgb(35, 35, 47)"
BrightTextColor = "rgb(255, 255, 255)"
HighlightColor = "rgb(74, 74, 103)"

MainSheet = """

QWidget#CentralWidget {
background-color: """ + BackgroundColor + """;
}



QWidget#TitleBar {
background-color: """ + TitleBarColor + """;
}

QWidget#ExitButton {
background-color: transparent;
}

QWidget::hover#ExitButton {
background-color: """ + ExitButtonColor + """;
}

QWidget#MinimizeButton {
background-color: transparent;
}

QWidget::hover#MinimizeButton {
background-color: """ + HighlightColor + """;
}

QWidget#Title {
color: """ + HighlightColor + """;
}



QWidget#NodeBox {
background-color: """ + MidColor + """;
}

QWidget#PropertyBox {
background-color: """ + MidColor + """;
border-radius: 5;
}

QWidget#PropertyTitle {
color: """ + BrightTextColor + """;
}



QWidget#Cycle {
background-color: """ + HighlightColor + """;
color: """ + BrightTextColor + """;
border-radius: 8;
}

"""