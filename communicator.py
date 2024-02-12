import rs232
import serial.tools.list_ports

class Communicator:
  def __init__(self) -> None:
    self.communicator = rs232.RS232C()

  def getCOMPorts(self):
    return [ports.device + " " + ports.description for ports in serial.tools.list_ports.comports()]

  def getPadsWeightByID(self, int_ID): # Array of weight
    pass

  def encoder(self, command) : 
    bls = [(len(command) + 2)] + list(bytearray(command,'utf-8'))
    print (bls)
    lc = 0
    for letter in bls:
      lc = lc ^ letter
    output = '\xF2' + command + chr(lc) + '\xF3'
    return output
  