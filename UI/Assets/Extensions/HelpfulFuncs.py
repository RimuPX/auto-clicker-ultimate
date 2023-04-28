from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QColor

def setShadow(widget: QWidget):
    ShadowEffect = QGraphicsDropShadowEffect()
    ShadowEffect.setBlurRadius(25)
    ShadowEffect.setColor(QColor(19, 50, 158, 100))
    ShadowEffect.setOffset(0, 3)

    widget.setGraphicsEffect(ShadowEffect)

def recolorPixmap(pixmap: QPixmap, color: QColor):
    tmpImage = pixmap.toImage()

    for x in range(tmpImage.width()):
        for y in range(tmpImage.height()):
            tmpImage.setPixelColor(x, y, QColor(color.red(), color.green(), color.blue(), tmpImage.pixelColor(x, y).alpha()))

    return QPixmap.fromImage(tmpImage)
