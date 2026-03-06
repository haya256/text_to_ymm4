#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テキスト → YMM4台本変換スクリプト
使い方:
  1. input.txt にテキストを保存
  2. python text_to_ymm4.py を実行
  3. script.csv が生成される
  4. YMM4の「ツール」→「台本編集」→「台本ファイルを開く」で読み込む
"""

import os
import re
import sys

# 設定
INPUT_FILE = "data/input.txt"
OUTPUT_FILE = "data/script.csv"
CHARACTER_NAME = "CHARACTER_NAME"  # YMM4に登録済みのキャラクター名に変更してください
MAX_CHARS = 40  # 1セリフの最大文字数（長すぎると読み上げが不自然になる）


def split_text(text):
    """テキストを適切な長さのセリフに分割する"""
    sentences = []

    # まず改行で分割
    lines = text.splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 句点・感嘆符・疑問符で分割
        parts = re.split(r'(?<=[。！？])', line)

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # 長すぎる場合はさらに分割（読点や接続詞で）
            if len(part) > MAX_CHARS:
                # 読点で分割を試みる
                sub_parts = re.split(r'(?<=[、])', part)
                current = ""
                for sub in sub_parts:
                    if len(current) + len(sub) <= MAX_CHARS:
                        current += sub
                    else:
                        if current:
                            sentences.append(current.strip())
                        current = sub
                if current.strip():
                    sentences.append(current.strip())
            else:
                sentences.append(part)

    return sentences


def convert_to_ymm4_script(input_path, output_path, character):
    """テキストファイルをYMM4台本形式に変換する"""
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"エラー: {input_path} が見つかりません。")
        print(f"テキストを {input_path} に保存してください。")
        sys.exit(1)

    sentences = split_text(text)

    if not sentences:
        print("エラー: テキストが空か、分割できませんでした。")
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for sentence in sentences:
            # YMM4台本形式: キャラ名[TAB]セリフ
            f.write(f"{character},{sentence}\n")

    print(f"完了！ {len(sentences)} 件のセリフを生成しました。")
    print(f"出力ファイル: {output_path}")
    print()
    print("次のステップ:")
    print("  YMM4を開いて「ツール」→「台本編集」→「台本ファイルを開く」")
    print(f"  → {output_path} を選択 → 「タイムラインに追加」をクリック")


if __name__ == "__main__":
    convert_to_ymm4_script(INPUT_FILE, OUTPUT_FILE, CHARACTER_NAME)
