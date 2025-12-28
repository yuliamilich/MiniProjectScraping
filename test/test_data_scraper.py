import sys
sys.path.insert(0, 'c:\\Users\\milic\\OneDrive\\Documents\\Study\\Semester 5\\הגנה לרשת\\MiniProjectSpearPhishing\\src')

from data_scraper import get_company

# Test the function with a sample query
if __name__ == "__main__":
    print("Testing get_company function...")
    
    # Test case 1: Valid name
    print("Test 1 - Valid name: 'Yulia Milich'")
    result = get_company("Yulia Milich")
    print(f"Result: {result}")
    print()
    
    # Test case 2: Empty string
    print("Test 2 - Empty string")
    result = get_company("")
    print(f"Result: {result}")
    print()
    
    # Test case 3: None value
    print("Test 3 - None value")
    result = get_company(None)
    print(f"Result: {result}")
    print()
    
    # Test case 4: Whitespace only
    print("Test 4 - Whitespace only")
    result = get_company("   ")
    print(f"Result: {result}")
    print()

    