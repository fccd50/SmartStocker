import PySimpleGUI as sg
import SmartDriver
import Shelf
import SmartInfo
import datetime
from queue import Queue
from threading import Thread

class SmartStocker:
  def __init__(self) -> None:
    self.to_SD_que = Queue()
    self.from_SD_que = Queue()
    self.info = SmartInfo.SmartInfo()
    self.shelves = [Shelf.Shelf(shelf) for shelf in self.info.get_Shelvs()]
    self.sd = SmartDriver.SmartDriver(self.to_SD_que, self.from_SD_que, self.info, self.shelves)
    self.in_weighing = False #"self.sd.on_com" is used as RS232 is on.
    self.in_monitor = False

  def run(self):
    # status_symbols = ['⚪','⚫','★','△']
    sg.theme("DarkBlue")
    sg.set_options(font=('Courier New', 20))
    tab_group = [[sg.Tab(shelf.SSName, shelf.shelf_gui(),expand_y=True)] for shelf in self.shelves]
    tab_group2= [[sg.Tab("Serial COM",[[sg.Text("Select COM Port")],[sg.Combo(self.sd.get_comportlist(), key="-comport-", size=(30,10)),sg.Button("COM Start",key="-StartCOM-")],[sg.Text("9600")],[sg.Text("Non Parity")],[sg.Text("Start/Stop 1bit no FLW control")]])], 
                 [sg.Tab("Twitter X", [[sg.Checkbox("Do you want to tweet in X?",key="-Xactive-")],[sg.Text("X Twitter Account Info")],[sg.InputText("uname",key="-XUserName-"), sg.Text("<- User Name")],[sg.InputText("xxxx@qqq.com",key="-XEmail-"), sg.Text("<- Your registerd Email or Telnumber")],[sg.InputText("xxxxxx",password_char='*',key="-Xpassword-"), sg.Text("<- Password")],[sg.Button("Set",key="-Xset-"),sg.Text("Not Ready", key="-Xready-")]])],
                 [sg.Tab("Log",[[sg.Multiline(key="-log-", autoscroll_only_at_bottom=True, expand_x=False, expand_y=True, horizontal_scroll=True)],[sg.Button("Save to a file?", key="-savebutton-")]])]
                 ]
    # n = 1 if self.info.get_ShelvsLen() < 7 else 3
    # print(self.info.get_ShelvsLen())
    layout = [[sg.Column([[sg.TabGroup(tab_group, border_width=0,key='TABGROUP')]],expand_x=True, expand_y=True, key="-CLMN1-")],[sg.HorizontalSeparator()],
      [sg.Column([[sg.Frame("All Smart Stockers", [shelf.shelf_gui_overall() for shelf in self.shelves],element_justification="TOP")]],vertical_scroll_only=True,scrollable=True, size=(400,400)),sg.TabGroup(tab_group2, expand_x=True, expand_y=True, border_width=0)],[sg.VPush()],[sg.HorizontalSeparator()],
      [sg.Button(' END ',key="-Exit-"),sg.Button('Save Parameteres?',key="-jasonsave-"), sg.Push(),sg.Text("RS232 is not started", key="-status-"),sg.Button('Start Weighing',key="-StartW-"),sg.Button('Start Monitor',key="-StartM-")]
      ]
    window = sg.Window("SmartStocker",layout,finalize=True,element_justification=("left"),scaling=True, size=(1920,1080))
    style = sg.ttk.Style()
    style.layout('TNotebook.Tab') # ,[] Hide tab bar
    window.maximize()
    # tr =  Thread(target=self.sd.do_measurement,daemon=True)

    self.gui_allupdate(window)
    while True:
      event, values = window.read(timeout=1000,timeout_key='-timeout-')
      if event in (sg.WINDOW_CLOSED, "-Exit-"):
        self.to_SD_que.put(True)
        window.close()
        break
      elif event == "-Xset-": # in future, please use thread to look better
        if self.sd.set_X(values["-XUserName-"],values["-XEmail-"],values["-Xpassword-"]) :
          window["-Xready-"].update("X is Ready.")
      elif event == "-StartCOM-":
        if values['-comport-'] != "" :
          com_num = values['-comport-'].split()[0]
          if self.sd.startSmartShelf(com_num):
            # sg.popup("Communication Started.", non_blocking=True, keep_on_top=True)
            window["-status-"].update("RS232 IS RUNNING.")
      elif event == "-savebutton-":
        path = sg.popup_get_folder("Save log to a file.", modal=False, keep_on_top=True,no_window=True)
        if path is not None:
          if self.sd.file_log(path, values["-log-"]) == False:
            sg.Popup("Not right path")
      elif event == "-StartW-":
        if self.sd.on_com:
          if self.in_weighing:
            self.in_weighing = False
            self.to_SD_que.put("STOP")
            self.tr.join()
            window["-status-"].update("IN PAUSE MODE   ")
            window["-StartW-"].update("Start Weighing")
          else:
            self.tr = self.thread_call()
            self.in_weighing = True
            window["-StartW-"].update("Stop Weighing")
            window["-status-"].update("IN WEIGHING MODE")
      elif event == "-StartM-":
        if not self.in_monitor:
          if self.sd.on_com and self.in_weighing :#RS232 and in weighing mode
            # sg.popup("Smart Stocker Started.", non_blocking=True, keep_on_top=True)
            window["-status-"].update("IN MONITORING")
            window["-StartM-"].update("Stop Monitor")
            self.in_monitor = True
        else:
          window["-status-"].update("IN WEIGHING MODE")
          window["-StartM-"].update("Stop Monitor")
          self.in_monitor = False
      elif event == "-timeout-":
        self.gui_allupdate(window)
      elif event in ["-Papw-"+str(pad) for shelf in self.shelves for pad in shelf.pads]:
        self.popup_newparameter(event, window, "APW:", 4)
      elif event in ["-Pthres-"+str(pad) for shelf in self.shelves for pad in shelf.pads]:
        self.popup_newparameter(event, window, "Threshold:", 10)
      elif event in ["GoTo:"+shelf.SSName for shelf in self.shelves]:
        window[event[5:]].select()
      elif event in ["-Pzerobutton-"+str(pad) for shelf in self.shelves for pad in shelf.pads]:
        if not self.in_weighing:
          temps = window[event].metadata
          if self.sd.set_zero(temps.split(":")[0],temps.split(":")[1]):
            sg.popup("Zero OK. Check it after weighing mode", non_blocking=True)
          else:
            sg.popup_error("Zero failed.", non_blocking=True)

  def thread_call(self)-> Thread:
        tr = Thread(target=self.sd.do_measurement,daemon=True)
        tr.start()
        return tr
    
  def popup_newparameter(self, event, window:sg, message:str, slice:int):
        text = sg.popup_get_text("New "+message+" ?", keep_on_top=True, modal=False, default_text=f"{window[event].DisplayText}"[slice:])
        if text != None:
          temp = text.replace(".","").replace(" ","")
          try:
            if temp.isnumeric():
              float(text) # in case of more than two "."
              window[event].update(message+text)
          except:
            pass
  def save_jayson(self):
    pass
    
  def gui_allupdate(self, window):
    for shelf in self.shelves:
      for pad in shelf.pads:
        pid = str(pad)
        if self.sd.on_com:
          if self.in_weighing:
            window["-Pzerobutton-"+pid](disabled=True)
            if self.in_monitor:
              window["-Pstatus-"+pid].update("Status:"+pad.status)
              window["-Pbar-"+pid].update(float(pad.weight)/pad.capacity)# later, it should be from pad instance
              if pad.outofstock() :
                window["-Pcount-"+pid](background_color="red")
                window["-Pfill-"+pid](text_color="red")
                if pad.in_short_waitfor_reset == False:
                  pad.in_short_waitfor_reset = True
                  txt = window["-log-"].get()
                  msg = "Shortage in "+ pad.name +" in " + shelf.SSName 
                  window["-log-"].print(txt+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S_"+msg)))
                  if window["-Xactive-"].get() and window["-Xready-"].get() =="X is Ready.":
                    self.sd.tweet(msg)
              else:
                window["-Pcount-"+pid](background_color="green")
                window["-Pfill-"+pid](text_color="white")
              window["-Pfill-"+pid].update(pad.get_status_symbol())
            else: # During not monitoring
              pass
          else: # During not in weighing mode 
            window["-Pzerobutton-"+pid](disabled=False)
        window["-Pweight-"+pid].update("Weight:"+pad.weight)
        window["-Pcount-"+pid].update("Count:"+str(pad.count))
        pad.set_apw(window["-Papw-"+pid].DisplayText[4:])
        pad.set_thres(window["-Pthres-"+pid].DisplayText[10:])
        # window["< PREV"].update(button_color = ('black','yellow'))
      
if __name__ == '__main__':
  ss = SmartStocker()
  ss.run()
