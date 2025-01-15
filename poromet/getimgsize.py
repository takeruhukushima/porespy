from skimage import io

def get_image_size(image_path):
    """
    画像を読み込み、(高さ, 幅) を返す関数
    """
    img = io.imread(image_path)
    # 画像がカラーの場合: shape は (height, width, channels)
    # グレースケールの場合: shape は (height, width)
    # いずれも width = shape[1], height = shape[0]
    height, width = img.shape[:2]
    return height, width

if __name__ == "__main__":
    path = "input_images/300x/0.5Pa250WTGB1umSi620C24h8N-NaOH30C4h1e-5N-HCl30C1.5h_m006.jpg"  # 画像ファイルのパスを指定
    h, w = get_image_size(path)
    print(f"画像の幅: {w} ピクセル")
    print(f"画像の高さ: {h} ピクセル")
