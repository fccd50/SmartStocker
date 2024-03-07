import Pad

class Shelf:
  def __init__(self, info):
    self.__ID = 0
    self.info = info

  @property
  def ID(self):
    return self.__ID
  @ID.setter
  def ID(self, id):
    self.__ID = id
  
  def _layout(self):
    pad = Pad.Pad()