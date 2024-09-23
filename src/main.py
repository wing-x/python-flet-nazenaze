from input_view import create_input_view
import flet as ft


def main(page: ft.Page):
    # 入力画面を作成する
    input_view = create_input_view(page)
    page.add(input_view)


ft.app(target=main)
