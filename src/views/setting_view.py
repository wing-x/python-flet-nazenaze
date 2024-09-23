import flet as ft


def create_settings_view(page: ft.Page, on_model_change):

    def on_dropdown_change(e):
        selected_value = max_naze.value
        print(f"選択された数値: {selected_value}")
        page.update()

    def on_api_model_change(e):
        selected_model = api_model_select.value
        on_model_change(selected_model)  # 選択されたモデルをコールバック関数に渡す
        page.update()

    api_model_select = ft.Dropdown(
        label="AIモデル",
        hint_text="AIモデルを選択してください",
        options=[
            ft.dropdown.Option("claude-3-5-sonnet-20240620"),
            ft.dropdown.Option("claude-3-opus-20240229"),
            ft.dropdown.Option("claude-3-sonnet-20240229"),
            ft.dropdown.Option("claude-3-haiku-20240307"),
            ft.dropdown.Option("TEST-DUMMY"),
        ],
        # デフォルト値は一旦ダミーにする
        # value="TEST-DUMMY",
        width=300,
        on_change=on_api_model_change,  # モデル選択の変更時のコールバックを追加
    )
    # 1から5での数値をドロップダウンの選択肢として生成
    options = [ft.dropdown.Option(str(i)) for i in range(1, 6)]

    # 最大深度
    max_naze = ft.Dropdown(
        label="最大深度(なぜの回数)",
        hint_text="最大深度(なぜの回数)を選択してください",
        options=options,
        value="5",
        width=200,
        # 正式に対応できるまで変更不可にする
        disabled=True,
        on_change=on_dropdown_change,
    )

    # 最大分岐数
    max_branch = ft.Dropdown(
        label="最大分岐数",
        hint_text="最大分岐数を選択してください",
        options=options,
        value="1",
        width=200,
        # 正式に対応できるまで変更不可にする
        disabled=True,
        on_change=on_dropdown_change,
    )

    return ft.Row(
        [
            api_model_select,
            ft.Container(height=20),
            max_naze,
            ft.Container(height=20),
            max_branch,
        ]
    )
