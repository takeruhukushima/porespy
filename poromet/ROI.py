import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from skimage import io

# 選択範囲の左上(x1, y1)と右下(x2, y2)
x1 = y1 = x2 = y2 = 0

def onselect(eclick, erelease):
    global x1, y1, x2, y2
    # もし eclick.xdata や erelease.xdata が None であれば、ドラッグが無効
    if eclick.xdata is None or erelease.xdata is None:
        print("ドラッグが正しく行われていません。画像の上でドラッグしてみてください。")
        return
    
    x1, y1 = int(eclick.xdata), int(eclick.ydata)
    x2, y2 = int(erelease.xdata), int(erelease.ydata)

    width = abs(x2 - x1)
    height = abs(y2 - y1)
    area = width * height

    print(f"選択された範囲: (x1={x1}, y1={y1}) → (x2={x2}, y2={y2})")
    print(f"幅: {width} px, 高さ: {height} px, 面積: {area} px^2\n")

def main():
    # 画像読み込み
    image_path = "input_images/ダウンロード.jpg"
    img = io.imread(image_path)

    fig, ax = plt.subplots()
    ax.imshow(img, cmap='gray')
    ax.set_title("ドラッグで範囲選択 → ピクセル数を計測")

    # drawtype='box' を明記, button=[1] を削除
    rect_selector = RectangleSelector(
        ax,
        onselect,
        useblit=False,
        minspanx=5,
        minspany=5,
        spancoords='data',
        interactive=True
    )

    plt.show()

if __name__ == "__main__":
    main()
