import PySimpleGUI as sg

def tab_layout(index):
    layout = [[sg.Text(f'Window {index+1}')]]
    return layout

sg.theme("DarkBlue")
sg.set_options(font=('Courier New', 16))

total, now = 5, 0

tab_group = [[sg.Tab(f"TAB {i}", tab_layout(i), key=f"TAB {i}")] for i in range(5)]
layout = [
    [sg.TabGroup(tab_group, border_width=0, pad=(0, 0), expand_x=True, expand_y=True, key='TABGROUP')],
    [sg.VPush()],
    [sg.Button('< PREV'), sg.Push(), sg.Button('Exit'), sg.Push(), sg.Button('NEXT >')],
]
window = sg.Window("Title", layout, finalize=True)
style = sg.ttk.Style()
style.layout('TNotebook.Tab', [])                           # Hide tab bar
window.maximize()

while True:

    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    elif event in ("< PREV", "NEXT >"):
        now = (now+1)%total if event == "NEXT >" else (now-1)%total
        window[f"TAB {now}"].select()

window.close()