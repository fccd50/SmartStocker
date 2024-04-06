from twikit import Client

class Logging:
  def __init__(self) -> None:
    self.client = Client("ja")

  def log_error(self, message:str):
    pass

  def twit_login(self, name:str, email:str, passwd:str)->bool:
    try:
      self.client.login(
        auth_info_1=name,auth_info_2=email,password=passwd
      )
      print ("OK")
      return True
    except:
      return False
    
  def sendmsg(self, msg:str):
    self.client.create_tweet(msg)
  

if __name__ == "__main__":
  lo = Logging()
  lo.twit_login("mettlertoleo", "mettlertoleo@yahoo.co.jp", "ubho1234")
  lo.sendmsg("Hello test again2")

  