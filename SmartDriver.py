import communicator 
import time
# import SmartInfo
# from threading import Thread
# from queue import Queue
import Logging

class SmartDriver():
  def __init__(self,dq, gq, shelves:list) -> None:
    self.from_SS_que = dq
    self.to_SS_que = gq
    self.cm = communicator.Communicator()
    # self.info = info
    self.log = Logging.Logging()
    self.shelves = shelves
    self.on_com = False

  # def set_info(self, info:SmartInfo):
  #   self.info = info
    
  def startSmartShelf(self, port:str)->bool:
    self.on_com = self.cm.open_communicator(port)
    return self.on_com
  
  def endSmartShelf(self):
    self.cm.close_communicator()

  def set_X(self, name:str, email:str, pawd:str)->bool:
    return self.log.twit_login(name, email, pawd)
  
  def tweet(self, msg:str):
    self.log.write_X_msg(msg)
  
  def set_zero(self, id:str, padnum:str)->bool:
    return self.cm.set_zero(id, padnum)

  def file_log(self, path:str, msg:str)->bool:
    return self.log.write_Log_msg(path, msg)

  def do_measurement(self):
    while True:
      time.sleep(0.5) 
      for shelf in self.shelves:
        re = self.cm.get_padsweight_byID_howmanypads(shelf.ID,shelf.howmanypads)
        for i, pad in enumerate(shelf.pads):
          if re != [] :
            pad.set_weight(re[i])
            # print ("dome "+re[i])
          time.sleep(0.05)
      try:
        if self.from_SS_que.get_nowait() == "STOP":
          print("stop q recieved")
          break
      except:
        pass
  def get_comportlist(self):
    return self.cm.getCOMPorts()


  