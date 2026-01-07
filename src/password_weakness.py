from pathlib import Path
from password_strength import PasswordPolicy, PasswordStats

def check_password_strength(password):
    stats = PasswordStats(password)
    print(f"Password Strength Score: {stats.strength()}")

    # Check against a specific policy
    policy = PasswordPolicy.from_names(strength=0.20) # Requires a score of at least 0.5
    results = policy.test(password)
    if results:
        print(f"Password failed policy check. Issues: {results}")
    else:
        print("Password passes policy check.")

def check_common_password(password, weak_passwords_path=None):
    """Return True if the password is found in the weak password list."""

    if password is None:
        return False

    candidate = str(password).rstrip("\n\r")
    wordlist_path = (
        Path(weak_passwords_path)
        if weak_passwords_path
        else Path(__file__).resolve().parent.parent / "rockyou_2025_00.txt"
    )

    if not wordlist_path.is_file():
        raise FileNotFoundError(f"Weak password list not found: {wordlist_path}")

    with wordlist_path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if candidate == line.rstrip("\n\r"):
                return True

    return False