# TODO なぜなぜ分を実行する前に、問題点が抽象的になってないかなどのチェック機能を入れる
import json
import os

import Dummy_API
import flet as ft
from nazenaze_analysis_api import perform_naze_naze_analysis
from result_view import create_result_view
from setting_view import create_settings_view


def create_input_view(page: ft.Page):
    page.title = "なぜなぜ分析アプリケーション"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1280
    page.window.height = 720
    page.padding = 20
    page.bgcolor = ft.colors.WHITE

    # 半透明の灰色を作成
    semi_transparent_blue = ft.colors.with_opacity(0.6, ft.colors.GREY_700)

    # メインビュー
    title = ft.Text("なぜなぜ分析アプリケーション", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)

    analysis_target = ft.TextField(
        label="なぜなぜ分析をする内容",
        multiline=True,
        min_lines=4,
        max_lines=4,
        label_style=ft.TextStyle(size=14, color=semi_transparent_blue),
        border_color=ft.colors.BLUE,
        focused_border_color=ft.colors.BLUE,
    )

    additional_info = ft.TextField(
        label="補足情報 ※開発中",
        multiline=True,
        min_lines=4,
        max_lines=4,
        label_style=ft.TextStyle(size=14, color=semi_transparent_blue),
        border_color=ft.colors.BLUE,
        focused_border_color=ft.colors.BLUE,
        disabled=True,
    )

    def show_alert_dialog(alert_title, content):
        def close_dialog(e):
            alert_dialog.open = False
            page.update()

        alert_dialog = ft.AlertDialog(
            title=ft.Text(alert_title),
            content=ft.Text(content),
            actions=[
                ft.TextButton("OK", on_click=close_dialog),
            ],
        )

        page.dialog = alert_dialog
        alert_dialog.open = True
        page.update()

    def on_run_analysis(e):
        # 設定したモデルデータを取得
        selected_model = api_model_select.value

        # 分析対象の問題のテキストを取得
        problem_text = analysis_target.value

        # 入力チェック
        if selected_model is None or selected_model == "":
            show_alert_dialog("警告", "AIモデルを選択してください。")
            return

        if not problem_text.strip():
            show_alert_dialog("警告", "なぜなぜ分析をする内容を入力してください。")
            return

        # プリント文で出力
        print(f"選択されたモデル: {selected_model}")
        print(f"分析対象の問題: {problem_text}")

        # ダミーを選択している場合にはテスト用の結果を表示する
        if selected_model == "TEST-DUMMY":
            # 実行時に相対パス一定にするため、input_viewsのあるファイル起点に移動する
            # これにより常にviewsフォルダを起点に参照する
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            data = Dummy_API.get_json_data("../models/claude_response_dummy_api.json")
            # 設定ビュー
            result_view = create_result_view(page, data)
            page.views.append(result_view)
            page.go("/result")
        else:
            # 選択したモデル、問題文にて出力を行う
            # TODO 出力結果の文章量によっては入りきらない場合があるので、リザルト画面について調整を行う
            model = selected_model
            user_problem = problem_text
            analysis_result = perform_naze_naze_analysis(user_problem, model)
            analysis_resul_json = json.loads(analysis_result[0].text)
            result_view = create_result_view(page, analysis_resul_json)
            page.views.append(result_view)
            page.go("/result")

    run_button = ft.ElevatedButton(
        "なぜなぜ分析を実行",
        on_click=on_run_analysis,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.GREEN,
        ),
    )

    # 設定ビュー
    def on_model_change(selected_model):
        # TEST-DUMMY以外のモデルが選択された場合、analysis_targetを有効化
        if selected_model == "TEST-DUMMY":
            analysis_target.disabled = True
            analysis_target.value = "新入社員の離職率が高い"
            additional_info.disabled = True
            additional_info.value = "特に無し"
        else:
            analysis_target.disabled = False
        page.update()

    # 設定ビューにon_model_change関数を渡す
    settings_view = create_settings_view(page, on_model_change)

    # api_model_selectをグローバルスコープで定義
    api_model_select = settings_view.controls[0]

    main_view = ft.Column(
        [
            ft.Container(
                content=title,
                bgcolor=ft.colors.BLUE_50,
                padding=10,
                border_radius=5,
            ),
            ft.Container(height=20),
            settings_view,
            ft.Container(height=20),
            analysis_target,
            ft.Container(height=20),
            additional_info,
            ft.Container(height=20),
            ft.Row([run_button]),
        ]
    )

    return main_view
