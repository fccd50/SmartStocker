import PySimpleGUI as sg
import time

layout = [[sg.Text("-Pname-")],
      [sg.Column([[sg.ProgressBar(100, orientation='v', expand_x=False, size=(20, 20))]])
      # sg.Column([sg.Text("-Pcapa-")],[sg.Text("-Pweight-")],[sg.Button("Setup")])]
      ]]
window = sg.Window('Progress Bar', layout)
while True:
   event, values = window.read()
   if event == sg.WIN_CLOSED or event == 'Exit':
      break
window.close()