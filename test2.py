import PySimpleGUI as sg
sg.theme('Light Brown 4')

# Define the LED characters
CIRCLE = '⚫'
CIRCLE_OUTLINE = '⚪'

def LED(color, key):
    """
    A user-defined element representing an LED indicator.

    Args:
        color (str): The color of the LED ('on' or 'off').
        key (str): A unique identifier for the LED element.

    Returns:
        sg.Text: The LED element.
    """
    return sg.Text(CIRCLE if color == 'on' else CIRCLE_OUTLINE, key=key, enable_events=True)
def func():
    print ("func")
dic={"led1":func}
# Create a simple window
layout = [
    [LED('on', 'led1'), sg.Text('LED 1')],
    [LED('off', 'led2'), sg.Text('LED 2',enable_events=True)],
    # Add more LED elements here if needed
    [sg.Button('Exit')]
]

window = sg.Window('LED Indicator', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == "led1":
        sg.popup("abd")
    print(event)
    func = dic[event]
    func()
window.close()