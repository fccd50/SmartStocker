import PySimpleGUI as sg

class Pad:
    def __init__(self) :
        self.__weight = 0.0
        self.__apw = 0.0
        self.__count = 0
        self.__thres = 0
    @property
    def weight(self):
        return self.__weight
    @weight.setter
    def weight(self,w):
        self.__weight = w