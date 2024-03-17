import serial

class RS232C:
  def __init__(self) :
    pass

  def connect(self, comport="COM8"):#default COM8
    try:
      # self.seri.setDTR(False)
      self.seri = serial.Serial(comport,9600) #, dsrdtr=True)
      self.seri.timeout=5
      self.seri.set_buffer_size = 100
      return True
    except:
      return False
    
  def disconnect(self):
    try:
      if (self.seri.isOpen) :
        self.seri.close()
    except:
      pass 

  def send_command(self, command):
    self.seri.write(command)

  def send_command_with_return(self, command):
    re = ""
    if self.seri.open :
      try:
        self.seri.write(command)
        re = self.seri.read_until(b"\xf3")
      except:
        print("RS232 exception")
    return re

if __name__ == "__main__":
  pass



