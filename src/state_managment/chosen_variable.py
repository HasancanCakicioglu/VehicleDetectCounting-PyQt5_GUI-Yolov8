
from enum import Enum

class Mask(Enum):
    MASK_1 = "assets/mask/traffic_mask.png"
    MASK_2 = "assets/mask/mask2.png"

class Line(Enum):
    LINE_1 = [0, 597, 1920, 597]
    LINE_2 = [950, 400, 950, 800]


class chosenVariable():
    def __init__(self):
        chosenVariable._List_MASK_NAME = ["Mask1", "Mask2", "Default"]
        chosenVariable._List_LINE_NAME = ["Line1", "Line2", "Default"]

        chosenVariable._MASK = Mask.MASK_1.value

        chosenVariable._LINE = Line.LINE_1.value

        chosenVariable._Speed_LIMIT = 40

    @staticmethod
    def controlLine(text:str):
        lines = chosenVariable.get_List_LINE_NAME()
        if text == lines[0]:
            chosenVariable.set_line(Line.LINE_1.value)
        elif text == lines[1]:
            chosenVariable.set_line(Line.LINE_2.value)
        else:
            chosenVariable.set_line(None)

    @staticmethod
    def controlMask(text:str):
        masks = chosenVariable.get_List_MASK_NAME()
        if text == masks[0]:
            chosenVariable.set_mask(Mask.MASK_1.value)
        elif text == masks[1]:
            chosenVariable.set_mask(Mask.MASK_2.value)
        else:
            chosenVariable.set_mask(None)

    @staticmethod
    def get_mask():
        return chosenVariable._MASK

    @staticmethod
    def set_mask(text):
        chosenVariable._MASK = text

    @staticmethod
    def get_line():
        return chosenVariable._LINE

    @staticmethod
    def set_line(text):
        chosenVariable._LINE=text


    @staticmethod
    def get_Speed_Limit():
        return chosenVariable._Speed_LIMIT

    @staticmethod
    def set_Speed_Limit(x:int):
        chosenVariable._Speed_LIMIT = x

    @staticmethod
    def get_List_MASK_NAME():
        return chosenVariable._List_MASK_NAME

    @staticmethod
    def get_List_LINE_NAME():
        return chosenVariable._List_LINE_NAME




