import PySimpleGUI as sg
from PIL import Image
import io
from glob import glob

image_dir = "images"         # 画像フォルダのパス
interval = 1000 * 3          # 画像切り替えインターバル(3秒)
exts = ["jpg", "png", "bmp"] # 表示する画像の拡張子
sg.theme("Black")            # カラーテーマ(背景色を黒にするため)
# 画面を最大化する場合
from screeninfo import get_monitors
monitor = get_monitors()[0]
window_size = (monitor.width, monitor.height)
# 画面を最大化しない場合(下の行の#を削除すること)
#window_size = (800, 600)

# リストの画像を表示し、indexにループ補正した値を返す
def show_image(window, images, index):
    image_size = (window_size[0] - 20, window_size[1] - 20) # 画像が若干見切れる対策
    # indexがマイナスならリストの上限値、indexがリスト上限より上なら0を設定する
    index = len(images) - 1 if index < 0 else 0 if index >= len(images) else index
    path = images[index]
    # 画像を縮小表示
    image = Image.open(path)
    image.thumbnail(image_size)
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    window["-IMAGE-"].update(data=bio.getvalue())
    return index

def main():
    # 画像リスト取得
    images = [x for ext in exts for x in glob(f"{image_dir}/*.{ext}")] # 内包表記2回で二次元配列を一次元に平坦化
    # ウィンドウ初期化
    layout = [
        [sg.Image(key="-IMAGE-", enable_events=True, expand_x=True, expand_y=True)],
    ]
    window = sg.Window("Image Viewer", layout, size=window_size, return_keyboard_events=True, finalize=True, no_titlebar=True)
    # メインループ
    index = show_image(window, images, 0) # ループ前に先頭の画像表示
    while True:
        event, values = window.read(timeout=interval)
        if event == "Exit" or event == sg.WIN_CLOSED or event.startswith("Escape"):
            break
        elif event == "__TIMEOUT__":
            index = show_image(window, images, index + 1)
        elif event == "-IMAGE-":
            # 画像コンポーネントクリックイベント
            widget = window["-IMAGE-"].Widget
            y = widget.winfo_pointery() - widget.winfo_rooty()
            if y < (window_size[1] // 10):
                if sg.popup_ok_cancel("終了しますか？") == "OK":
                    break
            x = widget.winfo_pointerx() - widget.winfo_rootx()
            if x < (window_size[0] // 2):
                index = show_image(window, images, index - 1)
            else:
                index = show_image(window, images, index + 1)
    window.close()

if __name__ == "__main__":
    main()


"""

'6t5    0.025 -   0.543I-    48.7IE10       E10       g'
'    0.025 -', '   0.543I- ', '   48.7IE10', '       E10 '

4(+/-)+8(数字)+1(エラー)
16
27
i*11+5:i*11+5+9

11*n+5
"""