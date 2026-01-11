import sys
import os
sys.path.insert(0, 'c:\\Users\\milic\\OneDrive\\Documents\\Study\\Semester 5\\הגנה לרשת\\MiniProjectSpearPhishing\\src')

from xml_fields import xml_to_list

# Test the function with a sample query
if __name__ == "__main__":
    print("Testing xml_to_list from file test_xml_fields.xml")

    # Get the directory where this test file is located
    test_dir = os.path.dirname(os.path.abspath(__file__))
    xml_file_path = os.path.join(test_dir, "test_xml_fields.xml")
    
    # Test 
    print("Test - test_xml_fields.xml")
    result = xml_to_list(xml_file_path)
    
    if result:
        for cred in result:
            print(f"Email: {cred.email}, Passwords: {cred.passwords}")
    print()
    