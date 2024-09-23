# MEMO 今後の仕様に合わせて柔軟に対応できるように別ファイルとして切り出しておく

import json

def get_json_data(json_data_path):
    with open(file=json_data_path,mode='r',encoding="utf-8") as f:
        data = json.load(f)
    return data
