import json

class SmartInfo:
  def __init__(self) -> None:
    try:
      with open("config.json", encoding="utf-8") as f:
        self.smart_dic = json.load(f)
    except:
      self.bad_jason = True

  def get_Len_each(self)->list:
    return [[self.smart_dic["SmartStocker"][i]["ID"]] for i in self.smart_dic["SmartStocker"]["ID"]]
            # len(self.smart_dic["SmartStocker"][i]["PADS"]) for i in self.smart_dic["SmartStocker"]["ID"]]

  def get_PadsLen_ByID(self, ID:int)->int:
    try:
      l = len(self.smart_dic["SmartStocker"][ID - 1]["PADS"])
    except:
      l = 0
    return l

  def get_ShelvsLen(self)->int:
    try:
      l = len(self.smart_dic["SmartStocker"])
    except:
      l = 0
    return l
  
  def get_RepeatList(self)->list:# int [[1,2],[2,4]] etc...
    return [[a["ID"]]+[len(a["PADS"])] for a in self.smart_dic["SmartStocker"]]
  
  def get_Shelvs(self):
    return self.smart_dic["SmartStocker"]
  
  def test(self):
    e = [[a["ID"]]+[len(a["PADS"])] for a in self.smart_dic["SmartStocker"]]
    print(e)

  def get_Shelf_names(self)->list:
    # return self.smart_dic["SmartStocker"][0]["SSName"]
    return [i["SSName"] for i in self.smart_dic["SmartStocker"]]
  
if __name__ == "__main__":
  si = SmartInfo()
  print (si.get_Shelf_names())
