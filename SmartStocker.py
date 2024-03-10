import PySimpleGUI as sg
# import communicator 
import Shelf
import SmartInfo

class SmartStocker:
  def __init__(self) -> None:
    # self.com = communicator()
    self.info = SmartInfo.SmartInfo()
    self.shelves = [Shelf.Shelf(a_shelf) for a_shelf in self.info.get_Shelvs()]

  def tab_layout(self,index):
    layout = [[sg.Text(f'Window {index+1}')]]
    return layout
  def run(self):
    sg.theme("DarkBlue")
    sg.set_options(font=('Courier New', 16))
    total, now = 5, 0
    tab_group = [[sg.Tab(f"TAB {i}", self.tab_layout(i), key=f"TAB {i}")] for i in range(5)]
    layout = [
            [sg.TabGroup(tab_group, border_width=0, pad=(0, 0), expand_x=True, expand_y=True, key='TABGROUP')],
            # [sg.Push()],
            [a.shelf_gui() for a in self.shelves],
            [sg.Button('< PREV'), sg.Push(), sg.Button('Exit'), sg.Push(), sg.Button('NEXT >')],
        ]
    window = sg.Window("Title", layout, finalize=True)
    style = sg.ttk.Style()
    style.layout('TNotebook.Tab', []) # Hide tab bar
    window.maximize()

    while True:
      event, values = window.read()
      if event in (sg.WINDOW_CLOSED, "Exit"):
        window.close()
        break
      elif event in ("< PREV", "NEXT >"):
        now = (now+1)%total if event == "NEXT >" else (now-1)%total
        window[f"TAB {now}"].select()

if __name__ == '__main__':
  ss = SmartStocker()
  ss.run()