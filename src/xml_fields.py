import xml.etree.ElementTree as ET
from Credentials import Credentials

def get_xml(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occured: {e}")

def xml_to_list(filename):
    xml_data = get_xml(filename)

    if not xml_data: 
        print(f"Error: xml_data is empty.")
        return []
    
    root = ET.fromstring(xml_data)
    credentials_map = {}  # Dictionary to group by email

    for url in root.findall('url'):
        params = {}
        # Extract all param tags
        for param in url.findall('param'):
            if param.text:
                # Parse "key=value" format
                key, value = param.text.split('=', 1)
                params[key] = value
        
        # Access email and password
        email = params.get('email', 'N/A')
        password = params.get('password', 'N/A')
        
        # Group by email - create Credentials object if not exists
        if email not in credentials_map:
            credentials_map[email] = Credentials(email)
        
        # Add password to the Credentials object
        credentials_map[email].add_password(password)
    
    # Return list of Credentials objects
    return list(credentials_map.values())

