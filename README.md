## Loopmata

[flet](https://github.com/flet-dev/flet)と[pyautogui](https://github.com/asweigart/pyautogui)を用いたデスクトップ自動操作ツール  

![Loopmata_ss_1204](https://github.com/d4ken/Loopmata/assets/112839844/614595d3-2024-48a0-9f37-cb8c60283d68)  

+ボタンでOperationを追加、実行時にはOperationに追加されている順番でLoop回繰り返す

### 機能
- 左クリック操作
- ドラッグ操作
- キー入力

### 開発環境
- Python 3.10.13
- conda 23.9.0
- PyCharm 2023.2.4 (Professional Edition)

## 導入手順
### STEP 1:　リポジトリをクローン
```bash
git clone https://github.com/d4ken/flet-automata.git
```
 
### STEP 2:　仮想環境の作成
```bash
conda create -n flet python=3.10
```
 
以下のコマンドを入力して仮想環境に入ります。
```bash
conda activate flet
```

### STEP: 実行
必要なライブラリをインストール
```bash
pip install -r requirements.txt
```
実行時は以下のコマンドを入力(ホットリロード)
```bash
flet run main.py -d
```

## MacOSで正常に動作しない場合
システム設定でTerminal.appのアクセシビリティ設定を有効化する必要があります。

システム設定 -> プライバシーとセキュリティ -> アクセシビリティ からTerminal.appを追加しトグルをオンにする
![アクセシビリティ設定](https://github.com/d4ken/flet-automata/assets/112839844/74500abd-b6c8-43bd-a520-12fd0fe75ae3)
