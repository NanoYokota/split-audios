#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音声ファイルを指定された長さで分割するスクリプト
"""
import argparse
import os
import sys
from pathlib import Path
from typing import List
from pydub import AudioSegment


def split_audio(
    input_path: str,
    chunk_length_sec: float,
    output_dir: str = "output"
) -> List[str]:
    """
    音声ファイルを指定された長さで分割する

    Args:
        input_path: 入力音声ファイルのパス
        chunk_length_sec: 分割する長さ(秒)
        output_dir: 出力ディレクトリ(デフォルト: "output")

    Returns:
        分割されたファイルのパスのリスト

    Raises:
        FileNotFoundError: 入力ファイルが存在しない場合
        ValueError: chunk_length_secが0以下の場合
    """
    # 入力ファイルの存在確認
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"入力ファイルが見つかりません: {input_path}")

    # chunk_length_secの検証
    if chunk_length_sec <= 0:
        raise ValueError(
            f"分割する長さは0より大きい必要があります: {chunk_length_sec}"
        )

    # 出力ディレクトリの作成
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 音声ファイルの読み込み
    print(f"音声ファイルを読み込んでいます: {input_path}")
    audio = AudioSegment.from_file(input_path)

    # ファイル情報の表示
    duration_sec = len(audio) / 1000  # ミリ秒から秒に変換
    print(f"音声の長さ: {duration_sec:.2f}秒")
    print(f"分割する長さ: {chunk_length_sec}秒")

    # 分割するチャンク数を計算
    chunk_length_ms = int(chunk_length_sec * 1000)  # 秒からミリ秒に変換
    total_chunks = (len(audio) + chunk_length_ms - 1) // chunk_length_ms
    print(f"分割数: {total_chunks}個")

    # ファイル名の準備
    input_file = Path(input_path)
    base_name = input_file.stem  # 拡張子を除いたファイル名
    extension = input_file.suffix  # 拡張子

    # 音声を分割して保存
    output_files = []
    print("\n分割を開始します...")

    for i in range(total_chunks):
        start_ms = i * chunk_length_ms
        end_ms = min((i + 1) * chunk_length_ms, len(audio))

        # チャンクを切り出し
        chunk = audio[start_ms:end_ms]

        # 出力ファイル名を生成(ゼロパディング)
        output_filename = (
            f"{base_name}_part{i + 1:03d}{extension}"
        )
        output_filepath = output_path / output_filename

        # チャンクを保存
        chunk.export(output_filepath, format=extension.lstrip("."))
        output_files.append(str(output_filepath))

        # 進捗表示
        chunk_duration = (end_ms - start_ms) / 1000
        print(
            f"  [{i + 1}/{total_chunks}] {output_filename} "
            f"({chunk_duration:.2f}秒) を保存しました"
        )

    print(f"\n完了! {len(output_files)}個のファイルに分割しました。")
    print(f"出力先: {output_path.resolve()}")

    return output_files


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="音声ファイルを指定された長さで分割します",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 音声ファイルを30秒ごとに分割
  python split_audio.py input/sample.mp3 30

  # 音声ファイルを5分ごとに分割
  python split_audio.py input/sample.mp3 5 -m

  # 音声ファイルを1.5分ごとに分割(小数点も可能)
  python split_audio.py input/sample.wav 1.5 --minutes

  # カスタム出力先を指定
  python split_audio.py input/sample.mp3 30 -o my_output
        """
    )

    parser.add_argument(
        "input_path",
        help="入力音声ファイルのパス"
    )

    parser.add_argument(
        "chunk_length",
        type=float,
        help="分割する長さ(デフォルト: 秒、-m/--minutesオプションで分に変更可能)"
    )

    parser.add_argument(
        "-m", "--minutes",
        action="store_true",
        help="分割する長さを分単位で指定する"
    )

    parser.add_argument(
        "-o", "--output",
        default="output",
        help="出力ディレクトリ(デフォルト: output)"
    )

    args = parser.parse_args()

    # 分単位の場合は秒に変換
    chunk_length_sec = args.chunk_length
    if args.minutes:
        chunk_length_sec = args.chunk_length * 60
        print(f"分割する長さ: {args.chunk_length}分 ({chunk_length_sec}秒)")

    try:
        split_audio(
            args.input_path,
            chunk_length_sec,
            args.output
        )
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(
            f"予期しないエラーが発生しました: {e}",
            file=sys.stderr
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

