import rs232
import serial.tools.list_ports

class Communicator:

  def __init__(self) -> None:
    self.serial = rs232.RS232C()
    self.serial.connect()

  def getCOMPorts(self):
    return [ports.device + " " + ports.description for ports in serial.tools.list_ports.comports()]

  def getPadsWeightByID(self, int_ID): # Array of weight
    pass

  def encoder(self, command) : 
    lh = len(command) + 2
    bls = [lh] + list(bytearray(command,'ascii'))
    lc = 0
    for letter in bls:
      lc = lc ^ letter
    output = b'\xF2' + bytes(chr(lh) + command + chr(lc),"ascii")+b"\xF3"
    # output.append(b'\xF3')
    # output.insert(0,b'\xF2')
    return output
  
  def getID(self):
    print(self.encoder("A"))
    # re =  self.serial.send_command_with_return(self.encoder("A"))
    # return self.serial.send_command_with_return(self.encoder("A"))
    # print (re)
  