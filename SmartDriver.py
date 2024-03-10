import communicator
import time
from threading import Thread
from queue import Queue

class SmartDriver():
  def __init__(self) -> None:
    self.data_q = Queue()
    self.onLine = self.cm = communicator.Communicator()

  def startSmartShelf(self, port:str):
    self.cm.open_communicator(port)
  def endSmartShelf(self):
    self.cm.close_communicator()

  def do_measurement(self):
    i = 0
    while True:
      print(self.cm.get_allPadWeight(1))
      try:
        if self.data_q.get_nowait():
          break
      except:
        pass


if __name__ == "__main__":
  sd = SmartDriver()
  sd.startSmartShelf("COM8")
  thred = Thread(target=sd.do_measurement,daemon=True).start()
  # sd.data_q.put(False)
  time.sleep(2)
  sd.data_q.put(True)
  sd.endSmartShelf()

  