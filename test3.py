import PySimpleGUI as sg

def make_main(x=None, y=None):
    # ------------ メインウィンドウ作成 ------------
    main_layout = [[sg.Text("メインウィンドウ")],
            [sg.Button("Hide Sub"), sg.Button("UnHide Sub")],
            [sg.Button("Disappear Sub"), sg.Button("Reappear Sub"), sg.InputText(key="inputs")],
            [sg.Button("Exit")],
            [sg.Button("set")]]
    return sg.Window("メインウィンドウ", main_layout, finalize=True, size=(300, 520), location=(x, y))


def make_sub(x=None, y=None):
    # ------------ サブウィンドウ作成 ------------
    sub_layout = [[sg.Text("サブウィンドウ")],
                [sg.Text("サブウィンドウが現れた！"), sg.Text("default", key="sub")],[sg.Button("subbtn")]
                ]
    return sg.Window("サブウィンドウ", sub_layout, finalize=True, size=(300, 120), location=(x, y))


main_window = make_main(800, 700)
sub_window = make_sub(800, 500)

while True:
    # 全てのウィンドウを読み込む
    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED or event == "Exit":
        break

    # Hideボタンが押された場合"
    elif event == "Hide Sub":
        sub_window.hide()
        print("Hideボタンで画面が隠されました")

    # UnHideボタンが押された場合
    elif event == "UnHide Sub":
        sub_window.un_hide()
        print("UnHideボタンで画面が現れました")

    # Disapparボタンが押された場合
    elif event == "Disappear Sub":
        sub_window.disappear()
        print("Disappearボタンで画面が隠されました")

    # Reappearボタンが押された場合
    elif event == "Reappear Sub":
        sub_window.reappear()
        print("Reappearボタンで画面が現れました")
    elif event == "set":
        print (values["inputs"])
        window["sub"].update(values["inputs"])
    elif event == "subbtn":
        print (values["inputs"])
