import flet as ft
from dashboard import DashboardPage
from globalModel import GlobalModel
from auth.login import Login
  # Import the second page
  # from the separate file
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
            
            
def show_error_dialog(page: ft.Page, title: str, message: str):
    dlg = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[
            ft.TextButton("OK", on_click=lambda e: close_dialog(page))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Dialog dismissed")
    )
    page.dialog = dlg
    dlg.open = True
    page.update()

def close_dialog(page: ft.Page):
    if page.dialog:
        page.dialog.open = False
    page.update()
def login_page(page: ft.Page):
    print("Initial route:", page.route)
    connection_status = connect_to_database()
    
    # Create controls first
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", width=300, password=True, can_reveal_password=True)
    login_button = ft.ElevatedButton(
        text="Login",
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
        ft.Column(
            [
                ft.Row([status_dot,status_text], alignment=ft.MainAxisAlignment.START),
                ft.Divider(height=9, thickness=3),
                
                ft.Image(src="images/icon.png", width=100, height=100,fit=ft.ImageFit.CONTAIN,),
                ft.Text("Welcome to FLowbit", size=30, weight=ft.FontWeight.BOLD, 
                       text_align=ft.TextAlign.CENTER, color="blue"),
                ft.Text("Please log in to continue", size=20, text_align=ft.TextAlign.CENTER),
                username,
                password, 
                login_button,
            ],
            
            # alignment=ft.MainAxisAlignment.CENTER,
            # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center, bgcolor='grey200',
        padding=20, width=380, height=430, border_radius=ft.border_radius.all(10)
    ), 
        
], horizontal_alignment=ft.CrossAxisAlignment.CENTER, vertical_alignment=ft.MainAxisAlignment.CENTER)
    

def go_to_dashboard(page: ft.Page, username: str, password: str):
    # Validate inputs first
    if not username or not password:
        show_error_dialog(page, "Validation Error", "Please enter both username and password")
        return
        
    login_instance = Login(username, password)
    result, message = login_instance.checkCredential()
    
    if result:
        page.go("/dashboard")
    else:
        show_error_dialog(page, "Login Failed", message)
    
# Current user state
current_user = {
    "id": None,
    "username": None,
    "is_authenticated": False,
    "permissions": []
}    

def main(page: ft.Page):
    # Page configuration
    page.window_full_screen = True
    page.title = "FLowbit"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    

    def route_change(e):
        print(f"Route change to: {e.route}")
        page.views.clear()
        
        if page.route == "/login":
            page.views.append(login_page(page))
            # Enable the login button again
            # login_button.disabled = False
        elif page.route == "/dashboard":
            if not any(v.route == "/dashboard" for v in page.views):
                dashboard = DashboardPage(page)
                page.views.append(
    ft.View(
        "/dashboard",
        controls=[dashboard.build()],
        appbar=dashboard.build_appbar()  # You need to expose the appbar from DashboardPage
    )
)
        
        page.update()

    def view_pop(e):
        print(f"View pop: {e.view.route}")
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Initialize with login page
    page.go("/login")
    

ft.app(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
