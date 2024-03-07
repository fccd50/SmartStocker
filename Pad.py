import PySimpleGUI as sg

class Pad:
    def __init__(self) :
        # self.__ID = 1
        self.__name = "Default"
        self.__padNum = 0
        self.__weight = 0.0
        self.__apw = 0.0
        self.__count = 0
        self.__thres = 0
        self.__or = 0
    @property
    def weight(self):
        return self.__weight
    @weight.setter
    def weight(self,w):
        self.__weight = w
    def _layout(self):
        return [[sg.Text(self.__name)],
                [sg.Text(f"W:{self.__weight}")]
                [sg.Button("buson", key=f"-B-{self.__ID}-{self.__padNum}")]
        ]
    