# 音声ファイル分割スクリプト

音声ファイルを指定された長さで分割するPythonスクリプトです。

## 機能

- 音声ファイルを指定された秒数または分数で分割
- 様々な音声フォーマットに対応(mp3, wav, ogg, flac, m4a など)
- 分割されたファイルを連番で自動命名
- 進捗状況の表示

## 必要な環境

- Python 3.8以上
- ffmpeg または libav

### ffmpegのインストール

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS
```bash
brew install ffmpeg
```

#### Windows
[ffmpegの公式サイト](https://ffmpeg.org/download.html)からダウンロードしてインストールしてください。

## セットアップ

1. リポジトリのクローン(または作業ディレクトリに移動)
```bash
cd /home/yohei-yokota/projects/split-audios
```

2. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本的な使い方

```bash
# 秒単位で分割(デフォルト)
python3 split_audio.py <音声ファイルのパス> <分割する長さ(秒)>

# 分単位で分割
python3 split_audio.py <音声ファイルのパス> <分割する長さ(分)> -m
```

### 使用例

#### 例1: 30秒ごとに分割
```bash
python3 split_audio.py input/sample.mp3 30
```

#### 例2: 5分ごとに分割
```bash
python3 split_audio.py input/podcast.mp3 5 -m
```

#### 例3: 1.5分ごとに分割(小数点も指定可能)
```bash
python3 split_audio.py input/podcast.mp3 1.5 --minutes
```

#### 例4: 10.5秒ごとに分割
```bash
python3 split_audio.py input/music.wav 10.5
```

#### 例5: カスタム出力ディレクトリを指定
```bash
python3 split_audio.py input/sample.mp3 30 -o my_output
```

### オプション

- `-m`, `--minutes`: 分割する長さを分単位で指定する
- `-o`, `--output`: 出力ディレクトリを指定(デフォルト: `output`)
- `-h`, `--help`: ヘルプメッセージを表示

## ディレクトリ構造

```
split-audios/
├── split_audio.py       # メインスクリプト
├── requirements.txt     # 依存パッケージ
├── README.md           # このファイル
├── input/              # 入力音声ファイルを配置するディレクトリ
└── output/             # 分割された音声ファイルが保存されるディレクトリ
```

## 出力ファイルの命名規則

分割されたファイルは以下の形式で命名されます:

```
<元のファイル名>_part001.<拡張子>
<元のファイル名>_part002.<拡張子>
<元のファイル名>_part003.<拡張子>
...
```

例: `sample.mp3`を分割した場合
- `sample_part001.mp3`
- `sample_part002.mp3`
- `sample_part003.mp3`

## サポートされている音声フォーマット

pydubとffmpegを使用しているため、以下のような多くの音声フォーマットに対応しています:

- MP3
- WAV
- OGG
- FLAC
- M4A
- AAC
- WMA
- その他、ffmpegがサポートするフォーマット

## トラブルシューティング

### エラー: "ffmpeg was not found"

ffmpegがインストールされていないか、パスが通っていません。上記の「ffmpegのインストール」セクションを参照してインストールしてください。

### エラー: "入力ファイルが見つかりません"

指定したファイルパスが正しいか確認してください。相対パスまたは絶対パスで指定できます。

### エラー: "分割する長さは0より大きい必要があります"

分割する長さには正の数を指定してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 開発

### 依存パッケージ

- `pydub`: 音声ファイルの操作
- `ffmpeg`: 音声ファイルのエンコード/デコード(システムレベル)
