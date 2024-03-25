import PySimpleGUI as sg

class Pad:
  def __init__(self, id, pad) :
    self.pad = pad # it is from json
    self.__ID = id
    self.__name = self.pad["PName"]
    self.__padNum = self.pad["PNum"]
    self.__apw = self.pad["APW"]
    self.__thres = self.pad["THRES"]
    self.__or = self.pad["OR"]
    self.__capa = self.pad["CAPA"]
    self.__picpath = self.pad["PICPATH"]
    self.__weight = 0.0 # for GUI, string.
    self.__count = 0
    self.__bar = 0
    self.status = "Not ready"

  @property
  def capacity(self):
    return self.__capa

  @property
  def weight(self):
    return str(self.__weight)
  @weight.setter
  def weight(self,w:str):
    temp = w.replace(".","").replace(" ","")
    if temp.isnumeric():
      self.__weight = float(w.replace(" ",""))
      print(f"in pad {self.__weight}")
      status = "Weighting"
    elif temp in "M":
      status = "In Motion"
    elif temp in "C":
      status = "Over"
    elif temp in "E":
      status = "Error"
    else:
      status = "Invalid"
    self.status = status

  @property
  def count(self):
    if self.__apw != 0:
      return str(int(self.__weight // self.__apw))
  
  def outofstock(self)->bool:
    if self.__or == "YES":
      return False
    else:
      return True if self.count < self.__thres else False

  def pad_gui(self):
    # each pad's gui has the object reference as string
    thisID = str(self)
    # print("in Pad "+thisID)
    return [[sg.Text(self.__name,key="-Pname-"+thisID)],
      [sg.Column([[sg.ProgressBar(1, orientation='v', expand_x=False, size=(20, 20),  key='-Pbar-'+thisID)]]),
      sg.Column([[sg.Text(f"Status:{self.status}",key="-Pstatus-"+thisID)],
      [sg.Text(f"Capacity:{self.__capa}",key="-Pcapa-"+thisID)],
      [sg.Text(f"Weight:{self.__weight}", key="-Pweight-"+thisID)],
      [sg.Text(f"APW:{self.__apw}",key="-Papw-"+thisID)],
      [sg.Text(f"Count:{self.__count}",key="-Pcount-"+thisID)],
      [sg.Text(f"Threshold:{self.__thres}",key="-Pthres-"+thisID,enable_events=True)],
      [sg.Button("Setup", key=f"-Psetupbutton-"+thisID)]])]
      ]
    