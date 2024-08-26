# これはサンプルの Python スクリプトです。
import json
import math
import re

# Shift+F10 を押して実行するか、ご自身のコードに置き換えてください。
# Shift を2回押す を押すと、クラス/ファイル/ツールウィンドウ/アクション/設定を検索します。


def print_hi(name):
    # スクリプトをデバッグするには以下のコード行でブレークポイントを使用してください。
    print(f"Hi, {name}")  # Ctrl+F8を押すとブレークポイントを切り替えます。


def calc(a, b):
    return a + b


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == "__main__":
    # print_hi("PyCharm")
    # tes = ["aaa", "bbb"]
    # tes = ",".join(tes).title()
    # print(tes)
    print(f"{3.14:3.1f}")
    tes = "abc123xyz"
    print(re.match("x.z", tes))
    print(re.search("x.z", tes))
    json_str = '{"a":123}'
    tes = json.loads(json_str)
    print(tes["a"])
# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
