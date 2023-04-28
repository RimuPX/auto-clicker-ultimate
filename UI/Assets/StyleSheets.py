from PyQt6.QtGui import QFont

class MainSheet:
    propertyFont = QFont("Sublima ExtraBold", 18)

    BackgroundColor = "rgb(255, 255, 255)"
    MidColor = "rgb(255, 255, 255)"
    TextColor = "rgb(32, 32, 42)"
    HighlightColor = "rgb(206, 228, 252)"
    BoxOutlineColor = "rgb(209, 215, 235)"
    ThemeColorBright = "rgb(154, 38, 226)"
    ThemeColorDark = "rgb(119, 38, 226)"

    CommonTextPadding = 5
    Sheet = """

    QWidget#CentralWidget {
    background-color: """ + BackgroundColor + """;
    }


    QWidget#Box {
    background-color: """ + BackgroundColor + """;
    border-radius: 5;
    border: 1px solid """ + BoxOutlineColor + """;
    }

    QWidget#PropertyTitle {
    color: """ + TextColor + """;
    }


    QWidget#Node {
    background-color: transparent;
    color: """ + TextColor + """;
    border-radius: 0;
    padding: """ + str(CommonTextPadding) + """px;
    }

    QWidget::hover#Node {
    background-color: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 """ + HighlightColor + """, stop:1 """ + MidColor + """);
    padding: """ + str(CommonTextPadding) + """px;
    }

    QWidget#SelectedNode {
    background-color: qlineargradient(spread:pad, x1:0 y1:0, x2:1 y2:0, stop:0 """ + ThemeColorBright + """, stop:1 """ + ThemeColorDark + """);
    color: """ + TextColor + """;
    border-radius: 0;
    padding: """ + str(CommonTextPadding) + """px;
    }

    """