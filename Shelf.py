import pysimplegui
import Pad

class Shelf:
  def __init__(self):
    self.__ID = 0

  @property
  def ID(self):
    return self.__ID
  @ID.setter
  def ID(self, id):
    self.__ID = id