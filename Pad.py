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
    self.__picpath = self.pad["PICPATH"] if self.checkpath(pad["PICPATH"]) else "pictures/nofile.png"
    self.__weight = 0.0 # for GUI, string.
    self.__count = 0
    self.__bar = 0
    self.in_short_waitfor_reset = False
    self.status = "Not ready"
    self.status_symbols = ['⚪','⚫','★','△']
    self.status_symbols_num = 0
    self.__keyID = str(self)

  @property
  def keyID(self):
    return self.__keyID
  @property
  def name(self):
    return self.__name

  def get_status_symbol(self)->str:
    return self.status_symbols[self.status_symbols_num]
  
  def checkpath(self, path)->bool:
    try :
      f = open(path)
      f.close()
      return True
    except:
      return False
  @property
  def capacity(self):
    return self.__capa
  
  def set_apw(self, text:str):
    self.__apw = float(text)
  def set_thres(self, text:str):
    self.__thres = int(text)

  @property
  def weight(self):
    return str(self.__weight)
  
  def set_weight(self,w:str)-> str:
    temp = w.replace(".","").replace(" ","")
    if temp.isnumeric():
      self.__weight = float(w.replace(" ",""))
      # print(f"in pad {self.__weight}")
      status = "Weighting" #if firstloop else "Weighting"
    elif temp in "M":
      status = "In Motion"
    elif temp in "C":
      status = "Over     "
    elif temp in "I":
      status = "Invalid  "
    else:
      status = "Error    "
    self.status = status

  @property
  def count(self)->int:
    if self.__apw > 0: 
      return self.__weight // self.__apw
  
  def outofstock(self)->bool:
    if self.__or == "YES":
      return False
    else:
      if self.count < self.__thres:
        self.status_symbols_num = 1
        # self.in_short_waitfor_reset = True # for twitter
        return True
      else:
        self.status_symbols_num = 0
        self.in_short_waitfor_reset = False
        return False

  def pad_gui(self):
    # each pad's gui has the object reference as string
    self.keyID = str(self)
    # print("in Pad "+self.keyID)
    return [[sg.Image(self.__picpath, size=(180,150) )],
      [sg.Text(self.__name,key="-Pname-"+self.keyID)],
      [sg.Column([[sg.ProgressBar(1, orientation='v', expand_x=False, size=(20, 20),  key='-Pbar-'+self.keyID)]]),
      sg.Column([[sg.Text(f"SCL Status:{self.status}",key="-Pstatus-"+self.keyID)],
      [sg.Text(f"Capacity:{self.__capa}",key="-Pcapa-"+self.keyID)],
      [sg.Text(f"Weight:{self.__weight}", key="-Pweight-"+self.keyID)],
      [sg.Text(f"APW:{self.__apw}",key="-Papw-"+self.keyID,enable_events=True)],
      [sg.Text(f"Count:{self.__count}",key="-Pcount-"+self.keyID)],
      [sg.Text(f"Threshold:{self.__thres}",key="-Pthres-"+self.keyID,enable_events=True)],
      [sg.Button("Setup", key=f"-Pzerobutton-"+self.keyID)]])]
      ]
  def pad_gui_overall(self):
    self.keyID = str(self)
    return sg.Text(self.status_symbols[self.status_symbols_num], key="-Pfill-"+self.keyID)
    