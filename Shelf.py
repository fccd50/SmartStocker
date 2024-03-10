import Pad
import PySimpleGUI as sg

class Shelf:
  def __init__(self, a_shelf):
    self.shelfinfo = a_shelf
    self.__ID = a_shelf["ID"]
    print(self.__ID)
    self.pads = [Pad.Pad(self.__ID, a_pad) for a_pad in self.shelfinfo["PADS"]]

  @property
  def ID(self):
    return self.__ID
  
  def shelf_gui(self):
    # for a in self.pads:
    #   sg.Column(a.pad_gui)
    return [[sg.Text(str(self.__ID))],[sg.Column(a.pad_gui()) for a in self.pads]]

