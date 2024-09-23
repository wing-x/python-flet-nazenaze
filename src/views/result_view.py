import flet as ft


class WhyWhyNode(ft.Column):
    def __init__(self, name, level, on_edit):
        super().__init__()
        self.name = name
        self.level = level
        self.on_edit = on_edit
        self.text_widget = ft.Text(self.name, size=14, width=150, text_align=ft.TextAlign.CENTER)

    def build(self):
        def get_group_color(level):
            colors = [ft.colors.BLUE_50, ft.colors.GREEN_50, ft.colors.YELLOW_50, ft.colors.RED_50, ft.colors.PURPLE_50]
            return colors[level % len(colors)]

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"なぜ？ (Level {self.level})", size=10, color=ft.colors.GREY_700),
                    self.text_widget,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=get_group_color(self.level),
            border_radius=5,
            padding=10,
            width=170,
            height=100,
            on_click=lambda _: self.on_edit(self),
        )

    def update_name(self, new_name):
        self.name = new_name
        self.text_widget.value = new_name
        self.update()


class Arrow(ft.Column):
    def build(self):
        return ft.Container(content=ft.Icon(ft.icons.ARROW_FORWARD, size=20), margin=ft.margin.only(top=20))


def create_result_view(
    page: ft.Page,
    data,
):
    def go_back(e):
        page.views.pop()
        page.go("/")

    def on_edit(node):
        def close_dialog(e):
            edit_dialog.open = False
            page.update()

        def save_edit(e):
            node.update_name(new_name.value)
            edit_dialog.open = False
            page.update()

        new_name = ft.TextField(value=node.name)
        edit_dialog = ft.AlertDialog(
            title=ft.Text("ノードを編集"),
            content=new_name,
            actions=[
                ft.TextButton("キャンセル", on_click=close_dialog),
                ft.TextButton("保存", on_click=save_edit),
            ],
        )

        page.overlay.append(edit_dialog)
        edit_dialog.open = True
        page.update()

    def create_chart(data):
        def create_row_node(val, level=0):
            node = WhyWhyNode(val, level, on_edit)
            row = ft.Row([node], alignment=ft.MainAxisAlignment.START, spacing=10)
            return row

        node_rows = ft.Row(spacing=10)

        result_col = ft.Column(spacing=50)
        if data["原因分析"]:
            level = 0
            for child in data["原因分析"]:
                val = list(child.values())[0]
                child_row = create_row_node(val, level + 1)
                if level == 0:
                    node_rows.controls.append(child_row)
                else:
                    node_rows.controls.extend([Arrow(), child_row])
                level += 1
        result_col.controls.append(node_rows)
        node_rows = ft.Row(spacing=10)
        if data["対策案"]:
            level = 0
            for child in data["対策案"]:
                val = list(child.values())[0]
                child_row = create_row_node(val, level + 1)
                if level == 0:
                    node_rows.controls.append(child_row)
                else:
                    node_rows.controls.extend([Arrow(), child_row])
                level += 1
        result_col.controls.append(node_rows)

        return result_col

    title = ft.Text("なぜなぜ分析結果", size=20.0, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)
    problem_title = ft.Text(f"問題点：{data["問題"]}", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.RED)
    back_button = ft.ElevatedButton("戻る", on_click=go_back)

    chart = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO)
    main_row = create_chart(data)
    chart.controls.append(main_row)

    content = ft.Column(
        [
            title,
            ft.Container(height=20),
            problem_title,
            ft.Container(height=20),
            chart,
            ft.Container(height=20),
            back_button,
        ]
    )

    return ft.View("/result", [content])
