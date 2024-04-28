import Pad
import PySimpleGUI as sg

class Shelf:
  def __init__(self, a_shelf):
    self.shelf = a_shelf
    self.__ID = a_shelf["ID"]
    self.__SSName = a_shelf["SSName"]
    self.__pads = [Pad.Pad(self.__ID, a_pad) for a_pad in self.shelf["PADS"]]
    self.__howmanypads = len(self.__pads)

  @property
  def pads(self):
    return self.__pads
  
  @property
  def howmanypads(self):
    return self.__howmanypads

  @property
  def ID(self):
    return self.__ID
  
  @property
  def SSName(self):
    return self.__SSName
  
  def shelf_gui(self)->list:
    return [sg.Text("ID:"+str(self.__ID) +":"+ self.__SSName)],[sg.Column(a.pad_gui()) for a in self.pads]
    # return [sg.Text("ID:"+str(self.__ID) +":"+ self.__SSName)],[a.pad_gui() for a in self.pads]

  def shelf_gui_overall(self)->list:
    rclick_menu =["menu",["GoTo:"+self.__SSName]]
    return [sg.Text("ID:"+str(self.__ID) +":"+ self.__SSName,enable_events=True, key=self.__SSName, right_click_menu=rclick_menu)], [pad.pad_gui_overall() for pad in self.pads]
    
