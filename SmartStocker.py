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
    self.sd = SmartDriver.SmartDriver(self.to_SD_que, self.from_SD_que, self.info)
    self.shelves = [Shelf.Shelf(a_shelf) for a_shelf in self.info.get_Shelvs()]

  def run(self):
    sg.theme("DarkBlue")
    sg.set_options(font=('Courier New', 20))
    tab_group = [[sg.Tab(a_shelf.SSName, a_shelf.shelf_gui(), key=a_shelf.SSName)] for a_shelf in self.shelves]
    layout = [
            [sg.TabGroup(tab_group, border_width=0, pad=(1, 1), expand_x=True, expand_y=True, key='TABGROUP')],
            [a.shelf_gui() for a in self.shelves],
            [sg.Button('< PREV'), sg.Push(),sg.Combo(self.sd.get_comportlist(), key="-comport-"), sg.Button("-StaCom-"),sg.Button('Exit'), sg.Button('NEXT >'), sg.Button('Start'), sg.Button('Stop')]
        ]
    window = sg.Window("SmartStocker",layout,finalize=True,element_justification=("left"),scaling=True)
    style = sg.ttk.Style()
    style.layout('TNotebook.Tab') # Hide tab bar
    window.maximize()

    while True:
      event, values = window.read(timeout=100,timeout_key='-timeout-')
      if event in (sg.WINDOW_CLOSED, "Exit"):
        window.close()
        break
      # elif event == "< PREV" or event == "NEXT >":
      #   now = (now+1)%2 if event == "NEXT >" else (now-1)%2
      #   window[f"TAB {now}"].select()
      elif event == "-StaCom-":
        if values['-comport-'] != "" :
          com_num = values['-comport-'].split()[0]
          self.sd.startSmartShelf(com_num)
        # sg.popup("Com OK", non_blocking=True, keep_on_top=True)
      elif event == "Start":
        Thread(target=self.sd.do_measurement,daemon=True).start()
        # sg.popup("start", non_blocking=True, keep_on_top=True)
      elif event == "Stop":
        # sg.popup("Stop", non_blocking=True, keep_on_top=True)
        self.to_SD_que.put(True)
      elif event == "-timeout-":
        try:
          a = self.from_SD_que.get(timeout=0.1)
          window["-Pweight-"+str(a[0])+"-"+str(a[1])].update(a[2])
        except:
          pass

if __name__ == '__main__':
  ss = SmartStocker()
  ss.run()
  # now = (now+1)%total if event == "NEXT >" else (now-1)%total