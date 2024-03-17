import communicator 
import time
import SmartInfo
from threading import Thread
from queue import Queue

class SmartDriver():
  def __init__(self,dq:Queue, gq:Queue, info:SmartInfo) -> None:
    self.from_SS_que = dq
    self.to_SS_que = gq
    self.cm = communicator.Communicator()
    self.info = info
  def set_info(self, info:SmartInfo):
    self.info = info
  def startSmartShelf(self, port:str):
    self.cm.open_communicator(port)
  def endSmartShelf(self):
    self.cm.close_communicator()

  def weight_parser(self,id:int, padnum:int, weightlist:list):
    # print(weightlist)
    for pad in range(padnum):
      if weightlist != [] :
        w = weightlist[pad].replace(" ","")
        self.to_SS_que.put([id, pad, w])
      else:
        self.to_SS_que.put([id, pad, ""])
    # print("parser"+str([id, padnum, t]))

  def do_measurement(self):
    i = 0
    while True:
      i += 1
      time.sleep(0.2)
      for a in self.info.get_RepeatList():
        re = self.cm.get_padsweight_byID_padnum(a[0],a[1])
        print(re)
        self.weight_parser(a[0],a[1],re)
        # for b in range(a[1]):
        time.sleep(0.01)
      # print(f"this count is {i}")
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
  thred = Thread(target=sd.do_measurement,daemon=True).start()
  time.sleep(100)
  sd.to_SS_que.put(True)
  sd.endSmartShelf()

  