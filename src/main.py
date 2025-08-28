import flet as ft
from dashboard import DashboardPage
from globalModel import GlobalModel
from auth.login import Login
from views.Profile import ProfilePage
from views.admin import Admin
from auth.fetch_user_permission import FetchUserPermission
from routes.allowed_routes import allowed_routes
from DialogMsg import DialogMsg
global_model = GlobalModel()


def connect_to_database():
        """Connect to the database and return the connection."""
        try:
            # Assuming globalModel has a method to connect to the database
            
            global_model = GlobalModel()
            if global_model.connect():
                print("Database connection established successfully!")
                return True
            else:
                print("Failed to connect to the database.")
                return False
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            
            

def login_page(page: ft.Page):
    print("Initial route:", page.route)
    connection_status = connect_to_database()
    
    # Create controls first
    username = ft.TextField(label="Username", border_width=1)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, border_width=1)
    login_button = ft.ElevatedButton(
        text="CONTINUE",
        width=200,
        on_click=lambda e: go_to_dashboard(page, username.value, password.value)
    )
    
    # Set initial button state based on connection
    if not connection_status:
        login_button.disabled = True

    status_dot = ft.CircleAvatar(
        bgcolor=ft.Colors.GREEN if connection_status else ft.Colors.RED, 
        radius=7
    )
    status_text = ft.Text(
        "ONLINE" if connection_status else "OFFLINE", 
        size=12, 
        color=ft.Colors.GREEN if connection_status else ft.Colors.RED
    )

    return ft.View("/login", [
        ft.Container(
            ft.Column([
                ft.Row([status_dot, status_text], alignment=ft.MainAxisAlignment.START),
                ft.Divider(height=9, thickness=3),
                ft.Row([
                    ft.Container(
                        content=ft.Image(src="images/flowbit_small-Photoroom.png", width=150, height=100, fit=ft.ImageFit.CONTAIN),
                        margin=ft.margin.only(top=0, bottom=0)
                    ),
], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.Text("LOG IN", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color="blue")
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(content = username, alignment=ft.alignment.center),
                ft.Container(content = password, alignment=ft.alignment.center),
                ft.Container(content = login_button, alignment=ft.alignment.center, margin=ft.margin.only(top=10, bottom=10)),

            ]),
            alignment=ft.alignment.center, bgcolor='grey200',
            padding=30, width=380, border_radius=ft.border_radius.all(10)
        ),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, vertical_alignment=ft.MainAxisAlignment.CENTER)
    

def go_to_dashboard(page: ft.Page, username: str, password: str):
    
    
    # Validate inputs first
    if not username or not password:
        dialog_instance = DialogMsg("Validation Error:", "Please enter both username and password to proceed.")
        dialog_instance.show_error_dialog(page)
        return
        
    login_instance = Login(username, password)
    result, message = login_instance.checkCredential()
    
    if result:
        page.go("/dashboard")
    else:
        dialog_instance = DialogMsg("Login Failed:", message)
        dialog_instance.show_error_dialog(page)
    
# Current user state
current_user = {
    "id": None,
    "username": None,
    "is_authenticated": False,
    "permissions": []
}    

async def main(page: ft.Page):
    # Page configuration
    page.window_full_screen = True
    page.title = "FLowbit"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    

    dashboard = None
    current_user = None

    async def set_main_content(content):
        if dashboard:
            # Rebuild the dashboard layout with the new main content
            page.views[-1].controls.clear()
            page.views[-1].controls.append(dashboard.build(content))
            page.update()

    async def route_change(e):
        nonlocal dashboard, current_user
        print(f"Route change to: {e.route}")
        if page.route not in allowed_routes:
            page.go("/login")
            return
        if page.route == "/login":
            page.views.clear()
            page.views.append(login_page(page))
        else:
            fetch_user_permission = FetchUserPermission()
            current_user = fetch_user_permission.current_user
            if not current_user or not current_user.get("is_authenticated"):
                page.go("/login")
                return
            if dashboard is None:
                dashboard = DashboardPage(page)
            if not page.views or page.views[-1].route != "/dashboard":
                page.views.clear()
                page.views.append(
                    ft.View(
                        "/dashboard",
                        controls=[dashboard.build()],
                        appbar=dashboard.build_appbar()
                    )
                )
            if page.route == "/dashboard":
                dash_content = ft.Container(
                content=ft.Image(src="images/flowbit_big.png"),
                alignment=ft.alignment.center  
                )
                await set_main_content(dash_content)
            elif page.route == "/profile":
                print("Navigating to Profile Page")
                profile_page = ProfilePage(page, current_user)
                await set_main_content(profile_page.main_content)
            elif page.route =="/admin":
                print("Navigating to Admin Page")
                admin_page = Admin(page, current_user)
                await set_main_content(admin_page.main_content)
            # Add more routes here as needed
        page.update()

    async def view_pop(e):
        print(f"View pop: {e.view.route}")
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Initialize with login page
    page.go("/login")
    

ft.app(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
