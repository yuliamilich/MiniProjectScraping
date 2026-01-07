import sys
sys.path.insert(0, 'c:\\Users\\milic\\OneDrive\\Documents\\Study\\Semester 5\\הגנה לרשת\\MiniProjectSpearPhishing\\src')

from password_weakness import check_password_strength, check_common_password

# Test the function with a sample query
if __name__ == "__main__":
    print("Testing check_password_strength and check_common_password function...")

    # Test case 1: qwerty123
    print("Test 1 - passwrod: 'qwerty123'")
    check_password_strength("qwerty123")
    result = check_common_password("qwerty123")
    print(f"Result: {result}")
    print()

    # Test case 2: P@sSw0rd!
    print("Test 2 - passwrod: 'P@sSw0rd!'")
    check_password_strength("P@sSw0rd!")
    result = check_common_password("P@sSw0rd!")
    print(f"Result: {result}")
    print()

    # Test case 3: abc123
    print("Test 3 - passwrod: 'abc123'")
    check_password_strength("abc123")
    result = check_common_password("abc123")
    print(f"Result: {result}")
    print()
    