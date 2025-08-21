from globalModel import GlobalModel

class FetchUserPermission:
    def __init__(self):
        self.global_model = GlobalModel()
        self.user_id = self.global_model.get_data('user_id')
        self.username = self.global_model.get_data('username')
        permissions = self.fetch_user_permissions(self.user_id)
        # Set is_authenticated True only if user_id and username are both present and not empty
        is_authenticated = bool(self.user_id and self.username)
        self.current_user = {
            "id": self.user_id,
            "username": self.username,
            "is_authenticated": is_authenticated,
            "permissions": permissions
        }
    # No view_pop handler; handled in main.py if needed
        
         
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
        self.global_model.set_data('permissions', permissions)
        return permissions
        
        
        