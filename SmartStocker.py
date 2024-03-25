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
    self.shelves = [Shelf.Shelf(a_shelf) for a_shelf in self.info.get_Shelvs()]
    self.sd = SmartDriver.SmartDriver(self.to_SD_que, self.from_SD_que, self.info, self.shelves)

  def run(self):
    Status_symbols = ['⚪','⚫','★','△']

    sg.theme("DarkBlue")
    sg.set_options(font=('Courier New', 20))
    tab_group = [[sg.Tab(a_shelf.SSName, a_shelf.shelf_gui(), key=a_shelf.SSName,expand_y=True)] for a_shelf in self.shelves]
    # This layout is without scroll bars. 
    layout = [[sg.TabGroup(tab_group, border_width=0, pad=(1, 1), expand_x=True, expand_y=True, key='TABGROUP')],
            # [a.shelf_gui() for a in self.shelves],
            [sg.Button('< PREV'), sg.Push(),sg.Combo(self.sd.get_comportlist(), key="-comport-"), sg.Button("COM Start",key="-StartCOM-"),sg.Button('Exit'), sg.Button('NEXT >'), sg.Button('Monitor'), sg.Button('Stop')]
          ]
    # This layout is when too many tabs habe to be shown with scroll bar. 
    # layout = [[sg.Column([
    #         [sg.TabGroup(tab_group, border_width=0, pad=(1, 1), expand_x=True, expand_y=True, key='TABGROUP')]],size_subsample_height=1, expand_x=True, expand_y=True, key="CLM")],
    #         # [a.shelf_gui() for a in self.shelves],
    #         [sg.Button('< PREV'), sg.Push(),sg.Combo(self.sd.get_comportlist(), key="-comport-"), sg.Button("COM Start",key="-StartCOM-"),sg.Button('Exit'), sg.Button('NEXT >'), sg.Button('Monitor'), sg.Button('Stop')]
    #     ]
    window = sg.Window("SmartStocker",layout,finalize=True,element_justification=("left"),scaling=True, size=(1920,1080))
    style = sg.ttk.Style()
    style.layout('TNotebook.Tab') # ,[] Hide tab bar
    window.maximize()

    while True:
      event, values = window.read(timeout=1000,timeout_key='-timeout-')
      if event in (sg.WINDOW_CLOSED, "Exit"):
        window.close()
        break
      # elif event == "< PREV" or event == "NEXT >":
      #   now = (now+1)%2 if event == "NEXT >" else (now-1)%2
      #   window[f"TAB {now}"].select()
      elif event == "-StartCOM-":
        if values['-comport-'] != "" :
          com_num = values['-comport-'].split()[0]
          self.sd.startSmartShelf(com_num)
          sg.popup("Com Started.", non_blocking=True, keep_on_top=True)
      elif event == "Monitor":
        Thread(target=self.sd.do_measurement,daemon=True).start()
        sg.popup("Monitor Started.", non_blocking=True, keep_on_top=True)
      elif event == "Stop":
        self.to_SD_que.put(True)
      elif event == "-timeout-":
        self.gui_allupdate(window)
      elif event == "< PREV":
        window["CLM"](background_color="green")#scrollable=True)
        

  def gui_allupdate(self, window):
    for shelf in self.shelves:
      for pad in shelf.pads:
        pid = str(pad)
        window["-Pweight-"+pid].update("Weight:"+pad.weight)
        window["-Pweight-"+pid](background_color="green")
        window["-Pstatus-"+pid].update("Status:"+pad.status)
        window["-Pcount-"+pid].update("Count:"+pad.count)
        window["-Pbar-"+pid].update(float(pad.weight)/pad.capacity)
      
    


if __name__ == '__main__':
  ss = SmartStocker()
  ss.run()
  # now = (now+1)%total if event == "NEXT >" else (now-1)%total