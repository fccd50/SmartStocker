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
    self.__capa = self.pad["CAPA"]
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
    return [[sg.Text(self.__name,key="-Pname-"+thisID)],
      [sg.Column([[sg.ProgressBar(100, orientation='v', expand_x=False, size=(20, 20),  key='-PBAR-')]]),
      sg.Column([[sg.Text(f"Capacity:{self.__capa}",key="-Pcapa-"+thisID)],
      [sg.Text(f"Weight:{self.__weight}", key="-Pweight-"+thisID)],
      [sg.Text(f"APW:{self.__apw}",key="-Papw-"+thisID)],
      [sg.Text(f"Count:{self.__count}",key="-Pcount-"+thisID)],
      [sg.Text(f"Threshold:{self.__thres}",key="-Pthres-"+thisID)],
      [sg.Button("Setup", key=f"-Psetupbutton-"+thisID)]])]
      ]
    