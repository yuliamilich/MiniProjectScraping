import xml.etree.ElementTree as ET
from Person import Person

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
        return {}
    
    root = ET.fromstring(xml_data)
    credentials_map = {}  # Dictionary to group by email

    for url in root.findall('url'):
        params = {}
        for param in url.findall('param'):
            if param.text:
                key, value = param.text.split('=', 1)
                params[key] = value
        
        email = params.get('email', 'N/A')
        password = params.get('password', 'N/A')
        
        if not password or not email:
            continue
        
        if email not in credentials_map:
            credentials_map[email] = []
        
        credentials_map[email].append(password)
    
    print(credentials_map)
    return credentials_map

