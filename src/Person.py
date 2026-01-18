class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.passwords = []
        self.company = ""
        self.password_score = 0
        self.repetitive_password = False

    def add_password(self, password):
        self.passwords.append(password)
    