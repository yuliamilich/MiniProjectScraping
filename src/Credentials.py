class Credentials:
    def __init__(self, email):
        self.email = email
        self.passwords = []

    def add_password(self, password):
        self.passwords.append(password)