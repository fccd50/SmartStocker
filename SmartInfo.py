import xml.etree.ElementTree as ET

class SmartInfo:
  def __init__(self) -> None:
    self.tree = ET.parse('config.xml')
  
  def getNumberOfPadsByID(self, intID):
    return 1
  
  def test(self):
    root = self.tree.getroot()
    print(root.tag)
    for child in root:
      print(child.tag)
      print(child.find("ID").text)
      print(str(len(child)))

if __name__ == "__main__":
  si = SmartInfo()
  si.test()