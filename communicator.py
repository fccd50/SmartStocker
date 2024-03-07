import rs232
import serial.tools.list_ports

class Communicator:
  def __init__(self) -> None:
    self.serial = rs232.RS232C()
    self.connected = self.serial.connect()
  def close_communicator(self):
    self.serial.disconnect()

  def getCOMPorts(self):
    return [ports.device + " " + ports.description for ports in serial.tools.list_ports.comports()] if self.connected else ""

  def getPadsWeightByID(self, int_ID): # Array of weight
    pass
  
  def paddingzero(self, id):
    l = len(id)
    if l == 1:
      id = "000"+id
    elif l == 2:
      id = "00" + id
    elif l == 3:
      id = "0" + id
    return id

  def encoder(self, command) : 
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
    print(self.encoder("A"))
    return self.serial.send_command_with_return(self.encoder("A")) if self.connected else ""

  def get_allPadWeight(self, id, n):
    self.serial.send_command_with_return(self.encoder(f"T"))
    pass
