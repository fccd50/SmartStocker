import json
# This class is a json handling.
class SmartInfo:
  def __init__(self) -> None:
    try:
      with open("config.json", encoding="utf-8") as f:
        self.smart_dic = json.load(f)
    except:
      self.bad_jason = True
  
  def update_pad_info(self,shelfid:str, pad_num:str, key:str, upd:str):
    for i, a_dic in enumerate(self.smart_dic["SmartStocker"]):
      if str(a_dic["ID"]) == shelfid:
        self.smart_dic["SmartStocker"][i]["PADS"][int(pad_num)][key] = float(upd)
        print(self.smart_dic)
        break

  def save_jason_file(self):
    with open("config.json", "wt") as f:
      json.dump(self.smart_dic,f, indent=2, ensure_ascii=False)

  def get_Len_each(self)->list:
    return [[self.smart_dic["SmartStocker"][i]["ID"]] for i in self.smart_dic["SmartStocker"]["ID"]]

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
  
  def get_RepeatList(self)->list:# int ID,padnum [[1,2],[2,4],[5,3]] etc...
    return [[a["ID"]]+[len(a["PADS"])] for a in self.smart_dic["SmartStocker"]]
  
  def get_Shelvs(self):
    return self.smart_dic["SmartStocker"]
  
  def test(self):
    e = [[a["ID"]]+[len(a["PADS"])] for a in self.smart_dic["SmartStocker"]]
    print(e)

  def get_Shelf_names(self)->list:
    return [i["SSName"] for i in self.smart_dic["SmartStocker"]]
  
  def get_Shelf_IDs(self)->list:
    return [i["ID"] for i in self.smart_dic["SmartStocker"]]
  
  def duplicate_checker(self):
    names = self.get_Shelf_names()
    IDs = self.get_Shelf_IDs()
    return len(names) != len(set(names)) or len(IDs) != len(set(IDs))


  
if __name__ == "__main__":
  si = SmartInfo()
  print (si.get_Shelf_names())
