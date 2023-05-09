from PyQt5.QtGui import QBrush, QColor


class Color_Constants():

    @staticmethod
    def get_Purple_Color():
        return tuple((255, 0, 255))

    @staticmethod
    def get_Red_Color():
        return tuple((255, 0, 0))

    @staticmethod
    def get_Orange_Color():
        return tuple((255, 165, 0))

    @staticmethod
    def get_Green_Color():
        return tuple((0,255, 0))

    @staticmethod
    def get_Blue_Color():
        return tuple((0,0,255))

    @staticmethod
    def get_Green_QBrush_Color():
        return QBrush(QColor(0, 255, 0, 127))

    @staticmethod
    def get_Red_QBrush_Color():
        return QBrush(QColor(255, 0, 0, 127))

