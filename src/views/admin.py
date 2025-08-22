import flet as ft
from globalModel import GlobalModel

class Admin:
    def __init__(self, page: ft.Page, current_user):
        self.page = page
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.sidebar_visible = True
        self.global_model = GlobalModel()
        self.current_user = current_user
        self.main_content = ft.Column(
            controls=[ft.Text("Welcome to Flowbit Admin!")],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER
        )

    def build(self):
        horizontal_divider = ft.Divider(height=1, color=ft.Colors.BLACK12)
        return ft.Column(
            controls=[
                horizontal_divider,
                ft.Row(
                    controls=[
                        self.main_content,
                    ],
                    expand=True,
                )
            ],
            expand=True,
        )