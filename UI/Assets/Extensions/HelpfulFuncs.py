from PyQt6.QtCore import QPoint
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

def linesOverlap(x1, x2, y1, y2):
    pos1 = (min(x1, x2), max(x1, x2))
    pos2 = (min(y1, y2), max(y1, y2))

    if pos2[0] < pos1[0] < pos2[1] or pos2[0] < pos1[1] < pos2[1] or \
            pos1[0] < pos2[0] < pos1[1] or pos1[0] < pos2[1] < pos1[1]: return True
def boxesOverlap(pos11: QPoint, pos12: QPoint, pos21: QPoint, pos22: QPoint):
    xOverlap = linesOverlap(pos11.x(), pos12.x(), pos21.x(), pos22.x())
    yOverlap = linesOverlap(pos11.y(), pos12.y(), pos21.y(), pos22.y())

    if xOverlap and yOverlap: return True
    return False