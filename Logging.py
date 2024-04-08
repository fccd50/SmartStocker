from twikit import Client
import datetime
# import csv

class Logging:
  def __init__(self) -> None:
    self.client = Client("ja")
    self.t = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    with open(".\\data\\"+self.t+".csv",mode="w", newline=None) as csv_file:
      csv_file.write("Date Time,What happened.\r\n")
    self.write_Log_msg("New Session Started.")

  def log_error(self, message:str):
    pass

  def twit_login(self, name:str, email:str, passwd:str)->bool:
    try:
      self.client.login(
        auth_info_1=name,auth_info_2=email,password=passwd
      )
      return True
    except:
      return False
    
  def write_X_msg(self, msg:str):
    t = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    self.client.create_tweet(msg)

  def write_Log_msg(self, msg:str):
    t = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    with open(".\\data\\"+self.t+".csv",mode="a",newline=None) as csv_file:
      csv_file.write(t + "," + msg+"\r\n")

  