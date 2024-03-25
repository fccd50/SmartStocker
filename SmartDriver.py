import communicator 
import time
import SmartInfo
from threading import Thread
from queue import Queue
import Logging

class SmartDriver():
  def __init__(self,dq:Queue, gq:Queue, info:SmartInfo, shelves:list) -> None:
    self.from_SS_que = dq
    self.to_SS_que = gq
    self.cm = communicator.Communicator()
    self.info = info
    self.log = Logging.Logging()
    self.shelves = shelves

  def set_info(self, info:SmartInfo):
    self.info = info
  def startSmartShelf(self, port:str):
    self.cm.open_communicator(port)
  def endSmartShelf(self):
    self.cm.close_communicator()

  def do_measurement(self):
    while True:
      time.sleep(0.5) #Exactly the same as below commented-out way. but weight value go to each pad object.
      for shelf in self.shelves:
        re = self.cm.get_padsweight_byID_howmanypads(shelf.ID,shelf.howmanypads)
        for i, pad in enumerate(shelf.pads):
          if re != [] :
            pad.weight = re[i]
            print ("dome "+re[i])
          time.sleep(0.05)
      try:
        if self.from_SS_que.get_nowait():
          print("stop q recieved")
          break
      except:
        pass
  def get_comportlist(self):
    return self.cm.getCOMPorts()

if __name__ == "__main__":
  dq = Queue()
  iq = Queue()
  i = SmartInfo.SmartInfo()
  sd = SmartDriver(dq, iq, i)
  sd.startSmartShelf("COM8")
  thred = Thread(target=sd.do_measurement,args=(i.get_Shelvs(),),daemon=True).start()
  time.sleep(100)
  sd.to_SS_que.put(True)
  sd.endSmartShelf()

  