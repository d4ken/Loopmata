## flet-automata
fletとpyautoguiを用いたデスクトップ自動操作ツール

![Loopmata_ss](https://github.com/d4ken/flet-automata/assets/112839844/f62fdc0f-880a-47b2-ae11-663df736e6f8)

### 機能
+ボタンでOperationを追加でき、実行時にはOperationに追加されている順番でLoop回繰り返す

- 左クリック操作
- ドラッグ操作
- キー入力

### 開発環境
### Mac:
- ProductName:    macOS
- CPU Architecture: arm64
- ProductVersion: 14.1.1
- BuildVersion:   23B81
- PyCharm 2023.2.4 (Professional Edition)
 
### 実行環境
- Python 3.10.13
- conda 23.9.0

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
