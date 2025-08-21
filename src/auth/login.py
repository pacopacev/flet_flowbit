# login_tab.py
import binascii
import re
from datetime import datetime
import bcrypt
from globalModel import GlobalModel



class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.global_model = GlobalModel()  # Create an instance of GlobalModel

    def checkCredential(self):
        try:
            if not self.global_model.connect():
                return [False, "Failed to connect to database!"]

            if not self.username or not self.password:
                return [False, "Username and password are required!"]

            query = "SELECT first_name, password FROM users WHERE first_name = %s;"
            user = self.global_model.execute_query_all(query, (self.username,))
        
            if not user:
                return [False, "User not found!"]

            stored_username, stored_password_hash = user[0]
        # Your password verification logic
            cleaned_hex_str = ''.join(re.findall(r'[0-9a-fA-F]+', stored_password_hash))
            bcrypt_bytes = binascii.unhexlify(cleaned_hex_str)
            bcrypt_hash = bcrypt_bytes.decode('utf-8')

            if bcrypt.checkpw(self.password.encode(), bcrypt_hash.encode()):
                self.get_user_id(user[0][0])
                self.login_insert(user[0][0])
                
                return [True, "Login successful!"]
            else:
                return [False, "Invalid password!"]

        except Exception as e:
            return [False, f"Login error: {str(e)}"]
        finally:
            self.global_model.close()
    def get_user_id(self, username):
        try:
            # SQL query to get the user ID based on the username
            query = "SELECT id FROM users WHERE first_name = %s;"
            params = (username,)

            # Fetch data from the database
            data = self.global_model.execute_query_all(query, params)

            # Check if user data was returned
            if data:
                user_id = data[0][0]  # ID of the user
                self.global_model.set_data('user_id', user_id)
                self.global_model.set_data('username', username)# Store user ID in global model
            else:
                print("No user found with that first name.")
        except Exception as e:
            # Handle any errors that occur during the process
            print(f"Error fetching user ID: {e}")
        
        
    def login_insert(self, username):
        try:
            # SQL query to get the user data based on the username
            query = "SELECT id, email FROM users WHERE first_name = %s;"
            params = (username,)

            # Fetch data from the database

            data = self.global_model.execute_query_all(query, params)

            # Check if user data was returned
            if data:
                # Get user ID and email from the first tuple in data
                user_id = data[0][0]  # ID of the user
                email = data[0][1]  # Email of the user
                created_at = datetime.now()  # Get the current datetime
                
                # Insert the user log entry
                log_data = (user_id, email, created_at)

                # Assuming insert_data method handles the insert logic
                columns = ['user_id', 'email', 'created_at']  # Column names in the user_log table
                self.global_model.insert_data("user_log", log_data, columns)

            else:
                print("No user found with that first name.")

        except Exception as e:
            # Handle any errors that occur during the process
            print(f"Error inserting user log: {e}")
