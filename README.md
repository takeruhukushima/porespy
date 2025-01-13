# poromet.py の実行手順 (ローカル)

このスクリプトは、与えられた画像の細孔径分布を計算します。ローカルで実行するには、以下の手順に従ってください。

1. **Python のインストール:** Python がインストールされていることを確認してください。

2. **必要なライブラリのインストール:** リポジトリのディレクトリで以下のコマンドを実行して、必要なライブラリをインストールします。
   ```bash
   pip install -r requirements.txt
   ```

3. **入力画像の準備:** 解析したい画像を `input_images` フォルダに配置し、ファイル名を `ダウンロード.jpg` に変更してください。

4. **スクリプトの実行:** リポジトリのディレクトリで以下のコマンドを実行します。
   ```bash
   python poromet.py
   ```

   実行後、細孔径分布の結果 (`pore_size_distribution.txt`) とセグメント化された画像 (`segmented_image.png`) が `output_data` フォルダに保存されます。

元のリポジトリのURL: https://github.com/PMEAL/porespy.git
