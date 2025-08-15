import flet as ft

class DashboardPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.LIGHT

    def build(self):
        # 1. Create the AppBar (correct capitalization)
        text_bar = ft.Text("Flowbit Dashboard")
        app_bar = ft.AppBar(
            leading=ft.Icon(ft.Icons.PALETTE),
            leading_width=40,
            title=text_bar,
            center_title=False,
            # bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, on_click=self.toggle_theme),
                ft.IconButton(ft.Icons.FILTER_3),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Settings"),
                        ft.PopupMenuItem(),  # Divider
                        ft.PopupMenuItem(
                            text="Dark Mode",
                            on_click=lambda e: self.toggle_theme(),
                        ),
                    ]
                ),
            ],
        )

        # 2. Create NavigationRail (sidebar)
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=80,
            min_extended_width=200,
            height=float("inf"),
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                    selected_icon=ft.Icons.ACCOUNT_CIRCLE,
                    label="Profile",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.BOOKMARK_BORDER,
                    selected_icon=ft.Icons.BOOKMARK,
                    label="Bookmarks",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Settings",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.LOGOUT_OUTLINED,
                    selected_icon=ft.Icons.LOGOUT,
                    label="Logout",
                ),
            ],
            on_change=self.controllerNavigation,
        )

        # 3. Main content area
        self.main_content = ft.Column(
            controls=[ft.Text("Welcome to Flowbit Dashboard!")],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        # 4. Combine all components
        self.page.appbar = app_bar
        return ft.Column(
            controls=[self.page.appbar,
                ft.Row(
                    controls=[
                        rail,
                        ft.VerticalDivider(width=1),
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