import communicator

if __name__ == '__main__':
  c = communicator.Communicator()
  a = c.getID()
  c.close_communicator()
  print(a)