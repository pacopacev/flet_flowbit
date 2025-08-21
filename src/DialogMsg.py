import flet as ft

class DialogMsg:
    def __init__(self, title, message):
        self.title = title
        self.message = message  
        
    def show_error_dialog(self, page: ft.Page):
        dlg = ft.AlertDialog(
            title=ft.Text(self.title, size=20, weight=ft.FontWeight.BOLD, color="red"),
            content=ft.Text(self.message),
            actions=[
                ft.ElevatedButton("OK", on_click=lambda e: close_dialog(page, dlg))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Dialog dismissed")
        )
        page.open(dlg)
        # print(f"Error: {message}")
        # snackbar = ft.SnackBar(ft.Text(f"{title}: {message}"))
        # page.open(snackbar)
        page.update()

def close_dialog(page: ft.Page, dlg: ft.AlertDialog):
    page.close(dlg)
    page.update()