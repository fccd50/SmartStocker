import Pad
import PySimpleGUI as sg

class Shelf:
  def __init__(self, a_shelf):
    self.shelfinfo = a_shelf
    self.__ID = a_shelf["ID"]
    self.__SSName = a_shelf["SSName"]
    # print(self.__ID)
    self.pads = [Pad.Pad(self.__ID, a_pad) for a_pad in self.shelfinfo["PADS"]]

  @property
  def ID(self):
    return self.__ID
  
  @property
  def SSName(self):
    return self.__SSName
  
  def shelf_gui(self)->list:
    return [[sg.Text("ID:"+str(self.__ID) +":"+ self.__SSName)],[sg.Column(a.pad_gui()) for a in self.pads]]
    # return [sg.Text("ID:"+str(self.__ID) +":"+ self.__SSName)],[a.pad_gui() for a in self.pads]

