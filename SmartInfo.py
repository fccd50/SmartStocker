import json

class SmartInfo:
  def __init__(self) -> None:
    with open("config.json", encoding="utf-8") as f:
      self.smart_dic = json.load(f)

  def get_PadsNum_ByID(self, intID)->int:
    try:
      l = len(self.smart_dic["SmartStocker"][intID-1]["PADS"])
    except:
      l = 0
    return l
  def get_ShelvsNum(self)->int:
    try:
      l = len(self.smart_dic["SmartStocker"])
    except:
      l = 0
    return l
  
  def test(self):
    print(self.smart_dic["SmartStocker"][0]["PADS"][0] )

if __name__ == "__main__":
  si = SmartInfo()
  si.test()
  print(si.get_ShelvsNum())