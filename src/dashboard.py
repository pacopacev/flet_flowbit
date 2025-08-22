import flet as ft
from globalModel import GlobalModel
from auth.fetch_user_permission import FetchUserPermission

class DashboardPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.sidebar_visible = True
        self.global_model = GlobalModel()
        self.current_user = FetchUserPermission().current_user

    def build_appbar(self):
        actions = []

        for permission in self.current_user["permissions"]:
            actions.append(
                ft.IconButton(
                    icon=permission["icon"],
                    tooltip=permission["name"],
                    on_click=(lambda _, route=permission["route"]: self.page.go(route))
                )
            )
        actions.append(ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="Item 1", checked=False,),
                ft.PopupMenuItem(),  # divider
                ft.PopupMenuItem(
                    text="Change Theme", checked=False, on_click=self.toggle_theme
                ),
            ]
        ))
        

        actions.append(ft.IconButton(ft.Icons.LOGOUT, tooltip="Logout", on_click=lambda _: self.logout()))
        
        return ft.AppBar(
            leading=ft.Container(
                content=ft.ElevatedButton(
                    "Dashboard", icon=ft.Icons.ARROW_BACK, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda _: self.page.go(self.page.views[-1].route)
                ),
                margin=ft.margin.only(left=10, top=10, bottom=10)
            ),
            leading_width=130,
            title=ft.Row(
                controls=[
                    ft.Text("Welcome", ),
                    ft.Text(f"{self.current_user['username']}", weight=ft.FontWeight.W_900, )
                ],
                
            ),
            # title=ft.Text(f"Welcome {self.current_user['username']}", weight=ft.FontWeight.W_900, ),
            # center_title=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=actions,
            
            
        )

    def build(self, main_content=None):
        if not hasattr(self, 'main_content') or self.main_content is None:
            self.main_content = ft.Column(
                controls=[ft.Text("Welcome to Flowbit Dashboard!")],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        if main_content is not None:
            # Replace all controls in main_content
            self.main_content.controls.clear()
            self.main_content.controls.append(main_content)
        
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.main_content,
                    ],
                    expand=True,
                )
            ],
            expand=True,
        )

    # No route_change method; all routing is handled in main.py

    def logout(self):
        print("Logging out...")
        # Clear user session data
        GlobalModel().set_data('user_id', None)
        GlobalModel().set_data('username', None)
        self.page.go("/login")

    def toggle_theme(self, e=None):
        self.page.theme_mode = (
            ft.ThemeMode.DARK 
            if self.page.theme_mode == ft.ThemeMode.LIGHT 
            else ft.ThemeMode.LIGHT
        )
        self.page.update()
        
    
        
    