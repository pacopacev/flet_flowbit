import flet as ft
from globalModel import GlobalModel
from auth.login import Login    

class DashboardPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.sidebar_visible = True
        self.global_model = GlobalModel()  # Create an instance of GlobalModel
        
        print(self.global_model.get_data('user_id'))
        self.user_id = self.global_model.get_data('user_id')
        self.fetch_user_permissions(self.user_id)
        # Current user state
        self.current_user = {
            "id": self.user_id,
            "username": self.global_model.get_data('username'),
            "is_authenticated": True,
            "permissions": self.fetch_user_permissions(self.user_id)
        }
        
    def fetch_user_permissions(self, user_id):
        permissions = []
        conn = None
        try:
            conn = self.global_model.connect()
            if not conn:
                return []

            query = """
                SELECT id, name, icon, route
                FROM flet_menus
                JOIN flet_user_permissions ON flet_menus.id = flet_user_permissions.menu_id
                WHERE flet_user_permissions.user_id = %s;
            """
            params = (user_id,)
            data = self.global_model.execute_query_all(query, params)
            for row in data:
                permissions.append({
                    "id": row[0],
                    "name": row[1],
                    "icon": row[2],
                    "route": row[3]
                })
            
        except Exception as e:
            print(f"Error fetching user permissions: {e}")
            return []
        finally:
            self.global_model.close()
        print(f"Fetched permissions: {permissions}")
        self.global_model.set_data('permissions', permissions)
        return permissions

    def build_appbar(self):
        if not self.current_user["is_authenticated"]:
            return ft.AppBar(
                title=ft.Text("Welcome Guest"),
                # actions=[
                #     ft.IconButton(ft.icons.LOGIN, on_click=lambda _: login(1))  # Using user_id=1 for demo
                # ]
            )
        
        # Build actions from permissions
        actions = []
        for permission in self.current_user["permissions"]:
            actions.append(
                ft.IconButton(
                    icon=permission["icon"],
                    tooltip=permission["name"],
                    # on_click=lambda e, route=permission["route"]: navigate_to(e, route)
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
            title=ft.Text(f"Welcome {self.current_user['username']}"),
            actions=actions
        )

    def build(self):
        self.main_content = ft.Column(
            controls=[ft.Text("Welcome to Flowbit Dashboard!")],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        horizontal_divider = ft.Divider(height=1, color=ft.Colors.BLACK12)
        return ft.Column(
            controls=[
                horizontal_divider,
                ft.Row(
                    controls=[
                        # rail if self.sidebar_visible else ft.Container(width=0),
                        # ft.VerticalDivider(width=1),
                        self.main_content,
                    ],
                    expand=True,
                )
            ],
            expand=True,
        )

    def controllerNavigation(self, e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            self.main_content.controls = [ft.Text("Profile Section")]
        elif selected_index == 1:
            self.main_content.controls = [ft.Text("Bookmarks Section")]
        elif selected_index == 2:
            self.main_content.controls = [ft.Text("Settings Section")]
        elif selected_index == 3:
            self.logout()
        self.page.update()

    def logout(self):
        print("Logging out...")
        self.page.go("/login")

    def toggle_theme(self, e=None):
        self.page.theme_mode = (
            ft.ThemeMode.DARK 
            if self.page.theme_mode == ft.ThemeMode.LIGHT 
            else ft.ThemeMode.LIGHT
        )
        self.page.update()