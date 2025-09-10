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
        self.table = ft.DataTable(
            width=1000,
            border=ft.border.all(2, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            heading_row_color=ft.Colors.BLACK12,
            heading_row_height=50   ,
            data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=200,
            columns=[
                ft.DataColumn(ft.Text("Id", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("First name", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Email", weight=ft.FontWeight.BOLD), numeric=True),
            ],
            rows=[
                
            ],
        )
        # self.users = self.get_users()
        
        
        self.add_user_button = ft.ElevatedButton(
                         "Add User",
                         icon=ft.Icons.ADD,
                         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                         on_click=lambda _: print("add user"),
                        
                     )
        
        
        
       
        
        self.main_content = ft.Column(
            #controls=[self.add_user_button, horizontal_devider, self.table],
            controls=[self.add_user_button, self.table],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER
        )
        


    def build(self):
        query = "SELECT * FROM users;"

        data = self.global_model.execute_query_all(query, params=None)
        for row in data:
            self.table.rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text(row[0]),),  # Id
            ft.DataCell(ft.Text(row[1])),  # First name
            ft.DataCell(ft.Text(row[2])),  # Email
        ]))
        horizontal_devider = ft.Divider()  
        self.main_content = ft.Column(
            controls=[self.add_user_button, horizontal_devider, self.table],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER
        )
        return self.main_content
    
    def get_users(self):
        pass

        
        # return data
        
    
        
    
    
    
 
  