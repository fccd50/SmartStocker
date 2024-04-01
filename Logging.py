from twikit import Client

class Logging:
  def __init__(self) -> None:
    self.client = Client("ja")

  def log_error(self, message:str):
    pass

  def tweet_login(self, name:str, email:str, passwd:str):
    self.client.login(
      auth_info_1=name,auth_info_2=email,password=passwd
    )
    