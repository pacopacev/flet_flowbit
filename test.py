import hashlib

def verify_password(password, hash):
    algorithm, iterations, salt, hashed_password = hash.split('$')
    iterations = int(iterations)
    salt = salt.encode('utf-8')
    password = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')

    derived_key = hashlib.pbkdf2_hmac('sha256', password, salt, iterations)
    return hashlib.sha256(derived_key).digest() == hashed_password

hash = "pbkdf2_sha256$600000$bCaV0fFH28w5nloqls2rle$Ef0kx9FmGT5I8WqOh0zjST0rOq9ZxXI2Cuz+qXlR3JY="
password = "your_password_here"

if verify_password(password, hash):
    print("Password is valid")
else:
    print("Password is invalid")