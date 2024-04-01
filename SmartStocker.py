import PySimpleGUI as sg
import SmartDriver
import Shelf
import SmartInfo
from queue import Queue
from threading import Thread

class SmartStocker:
  def __init__(self) -> None:
    self.to_SD_que = Queue()
    self.from_SD_que = Queue()
    self.info = SmartInfo.SmartInfo()
    self.shelves = [Shelf.Shelf(shelf) for shelf in self.info.get_Shelvs()]
    self.sd = SmartDriver.SmartDriver(self.to_SD_que, self.from_SD_que, self.info, self.shelves)
    self.in_monitor = False

  def run(self):
    # status_symbols = ['⚪','⚫','★','△']
    sg.theme("DarkBlue")
    sg.set_options(font=('Courier New', 20))
    tab_group = [[sg.Tab(shelf.SSName, shelf.shelf_gui(),expand_y=True)] for shelf in self.shelves]
    n = 1 if self.info.get_ShelvsLen() < 7 else 3
    print(self.info.get_ShelvsLen())
    layout = [[sg.Column([[sg.TabGroup(tab_group, border_width=0,key='TABGROUP')]],expand_x=True, expand_y=True, key="-CLMN1-")],[sg.HorizontalSeparator()],
      [sg.Column([[sg.Frame("All Smart Stockers", [shelf.shelf_gui_overall() for shelf in self.shelves],element_justification="TOP")]],vertical_scroll_only=True,scrollable=True, size=(400,400))],[sg.VPush()],
      [sg.Button('< PREV'),sg.Push(),sg.Combo(self.sd.get_comportlist(), key="-comport-"),sg.Button("COM Start",key="-StartCOM-"),sg.Button('Exit'), sg.Button('NEXT >'), sg.Button('Monitor'), sg.Button('Stop')]
      ]
    window = sg.Window("SmartStocker",layout,finalize=True,element_justification=("left"),scaling=True, size=(1920,1080))
    style = sg.ttk.Style()
    style.layout('TNotebook.Tab') # ,[] Hide tab bar
    window.maximize()
    tr =  Thread(target=self.sd.do_measurement,daemon=True)

    while True:
      event, values = window.read(timeout=1000,timeout_key='-timeout-')
      if event in (sg.WINDOW_CLOSED, "Exit"):
        self.to_SD_que.put(True)
        window.close()
        break
      elif event == "-StartCOM-":
        if values['-comport-'] != "" :
          com_num = values['-comport-'].split()[0]
          self.sd.startSmartShelf(com_num)
          tr.start()
          sg.popup("Communication Started.", non_blocking=True, keep_on_top=True)
      elif event == "Monitor":
        sg.popup("Smart Stocker Started.", non_blocking=True, keep_on_top=True)
        self.in_monitor = True
      elif event == "Stop":
        self.in_monitor = False
        self.to_SD_que.put(True)
      elif event == "-timeout-":
        self.gui_allupdate(window)
      elif event == "< PREV":
        print(["-Papw-"+str(pad) for shelf in self.shelves for pad in shelf.pads])
        # window["CLM"].update(background_color="green")#scrollable=True) it is NOT working....
      elif event in ["-Papw-"+str(pad) for shelf in self.shelves for pad in shelf.pads]:
        self.popup_newparameter(event, window, "APW:", 4)
      elif event in ["-Pthres-"+str(pad) for shelf in self.shelves for pad in shelf.pads]:
        self.popup_newparameter(event, window, "Threshold:", 10)
      elif event in ["GoTo:"+shelf.SSName for shelf in self.shelves]:
        window[event[5:]].select()

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

  def gui_allupdate(self, window):
    for shelf in self.shelves:
      for pad in shelf.pads:
        pid = str(pad)
        window["-Pweight-"+pid].update("Weight:"+pad.weight)
        window["-Pcount-"+pid].update("Count:"+str(pad.count))
        if self.in_monitor :
          if pad.outofstock() :
            window["-Pcount-"+pid](background_color="red")
            window["-Pfill-"+pid].update(pad.get_status_symbol())
          else:
            window["-Pcount-"+pid](background_color="green")
        window["-Pstatus-"+pid].update("Status:"+pad.status)
        window["-Pbar-"+pid].update(float(pad.weight)/pad.capacity)# later, it should be from pad instance
        pad.set_apw(window["-Papw-"+pid].DisplayText[4:])
        pad.set_thres(window["-Pthres-"+pid].DisplayText[10:])
        # window["< PREV"].update(button_color = ('black','yellow'))
      
    


if __name__ == '__main__':
  ss = SmartStocker()
  ss.run()
  # now = (now+1)%total if event == "NEXT >" else (now-1)%total