import rs232
import serial.tools.list_ports
# from threading import Thread
# import time

class Communicator:
  def __init__(self) -> None:
    self.connected = False

  def open_communicator(self, comport:str):
    self.serial = rs232.RS232C()
    self.connected = self.serial.connect(comport)
  def close_communicator(self):
    self.serial.disconnect()

  def getCOMPorts(self) -> list:
    return [ports.device + " " + ports.description for ports in serial.tools.list_ports.comports()] #if self.connected else []
  
  def paddingzero(self, id:int) -> str:
    l = len(id)
    if l == 1:
      id = "000"+id
    elif l == 2:
      id = "00" + id
    elif l == 3:
      id = "0" + id
    return id

  def encoder(self, command) -> bytearray : 
    if self.connected:
      lh = len(command) + 2
      bls = [lh] + list(bytearray(command,'ascii'))
      lc = 0
      for letter in bls:
        lc = lc ^ letter
      output = b'\xF2' + bytes(chr(lh) + command + chr(lc),"ascii")+b"\xF3"
    else:
      output = ""
    return output
  
  def getID(self):
    # print("getDI in comter "+self.encoder("A"))
    return self.serial.send_command_with_return(self.encoder("A")) if self.connected else ""

  def get_padsweight_byID(self, id:int)->list:# str list
    if self.connected:
      command = self.encoder("T"+self.paddingzero(str(id))+"#")
      returnBstring = self.serial.send_command_with_return(command)
      l = (len(returnBstring)-4)//11 # how many answered pads in 
      return [returnBstring[i*11+5:i*11+5+9].decode() for i in range(l)]
    
  def get_padsweight_byID_howmanypads(self, id:int, pads:int)->list:# str list
    if self.connected:
      command = self.encoder("T"+self.paddingzero(str(id))+str(pads))
      returnBstring = self.serial.send_command_with_return(command)
      # print("returnBstring")
      # print(returnBstring)
      l = (len(returnBstring)-4)//11 # how many answered pads in 
      return [returnBstring[i*10+4:i*10+14].decode() for i in range(l)]

  def test_thread(self):
    count = 0
    while True:
      if count > 100:
        break
      print(c.get_padsweight_byID_padnum(1,1))
      time.sleep(0.01)
      print(c.get_padsweight_byID_padnum(2,2))
      time.sleep(0.01)
      count += 1
    print("end test")
    self.close_communicator()

if __name__ == "__main__":
  c = Communicator()
  c.open_communicator("COM8")
  Thread(target=c.test_thread,daemon=True).start()
  input("stop?")
