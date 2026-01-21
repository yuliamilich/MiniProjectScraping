from password_strength import PasswordStats

def check_password_strength(password):
    stats = PasswordStats(password)
    return stats.strength()

def check_common_password(password, weak_passwords_path="config/rockyou_2025_00.txt"):
    """Return True if the password is found in the weak password list."""

    if password is None:
        return False

    candidate = str(password).rstrip("\n\r")

    try:
        with open(weak_passwords_path, 'r') as file:
            for line in file:
                if candidate == line.rstrip("\n\r"):
                    return True
    except FileNotFoundError:
        print(f"Error: The file '{weak_passwords_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return False
