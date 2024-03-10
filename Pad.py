import PySimpleGUI as sg

class Pad:
  def __init__(self, id, pad) :
    self.pad = pad
    self.__ID = id
    self.__name = self.pad["PName"]
    self.__padNum = self.pad["PNum"]
    self.__apw = self.pad["APW"]
    self.__thres = self.pad["THRES"]
    self.__or = self.pad["OR"]
    self.__picpath = self.pad["PICPATH"]
    self.__weight = 0.0
    self.__count = 0
    # print(type(self.__ID))

  @property
  def weight(self):
    return self.__weight
  @weight.setter
  def weight(self,w):
    self.__weight = w
  def pad_gui(self):
    thisID = str(self.__ID) + "-"+ str(self.__padNum)
    print(thisID)
    return [[sg.Text(self.__name)],
      [sg.Text(f"Weight:{self.__weight}", key="-W-"+thisID)],
      [sg.Button("buson", key=f"-B-"+thisID)]
      ]
    