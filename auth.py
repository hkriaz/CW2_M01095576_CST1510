import bcrypt
import os

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")  # store as string

def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def register_user(username, password):
    hashed_password = hash_password(password)
    with open("users.txt", "a") as f:
        f.write(f"{username}:{hashed_password}\n")
    print(f"{username} registered successfully!")

def login_user(username, password):
    if not os.path.exists("users.txt"):
        print("No users registered yet.")
        return False

    with open("users.txt", "r") as f:
        for line in f:
            user, hash1 = line.strip().split(":", 1)
            if user == username:
                if verify_password(password, hash1):
                    print("Login successful!")
                    return True
                else:
                    print("Invalid password.")
                    return False
    print("Username not found.")
    return False

def main():
    option = input("Sign up or Login? ").strip().lower()
    username = input("Username: ")
    password = input("Password: ")

    if option == "sign up":
        register_user(username, password)
    elif option == "login":
        login_user(username, password)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
