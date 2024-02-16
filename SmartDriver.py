import abc
import communicator

class SmartDriver(metaclass=abc.ABCMeta):
  def __init__(self) -> None:
    self.cm = communicator.Communicator()
  @abc.abstractmethod
  def run():
    pass

class Ev_Monitor(SmartDriver):
  def run():
    pass
