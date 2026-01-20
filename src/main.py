from Person import Person
from data_scraper import get_company
from send_email import send_phishing_email, send_phishing_info_email
from xml_fields import xml_to_list
from password_weakness import check_common_password, check_password_strength
from listen_to_new_files import receive_new_report
import threading
import json

PROMPT = (
    "Choose from these options: "
    "1. Enter one person. "
    "2. Enter path to file with many people. "
    "q. quit the program. "
    "> "
)
DEFAULT_PATH_TO_LIST='config/list_to_attack.txt'
PATH_TO_REPORTS='SharedDir/reports/'

def is_valid_person(name: str, email: str) -> bool:
    return bool(name) and bool(email) and "@" in email

def attack_person(people_map, map_lock, name, email, fake_url):
    if not is_valid_person(name, email):
        print(f"[WARN] Skipping invalid person: name='{name}', email='{email}'")
        return
    
    company = get_company(name)

    with map_lock:
        people_map[email] = Person(name, email)
        people_map[email].company = company
    
    send_phishing_email(name, email, company, fake_url)

def user_side(people_map, map_lock, shutdown, fake_url):
    while not shutdown.is_set():
        cmd = input(PROMPT).strip()
        if cmd == "q":
            shutdown.set()
            break
        if cmd == "1":
            person = input("> Enter 'name' and 'email' (Seperate by using '' around each): ")
            parts = person.split("' '")
            if len(parts) != 2:
                print("[WARN] Bad format. Please try again.")
                continue
            name = parts[0].strip("'")
            email = parts[1].strip("'")
            attack_person(people_map, map_lock, name, email, fake_url)
        if cmd == "2":
            file_path = input("> Enter path to a file with names and emails (each line has name in double ' and email in double ') (default file: config/list_to_attack.txt): ")
            if not file_path:
                file_path=DEFAULT_PATH_TO_LIST
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split('" "')
                    if len(parts) != 2:
                        print("[WARN] Bad format. Please try again.")
                        continue
                    name = parts[0].strip('"')
                    email = parts[1].strip('"')
                    attack_person(people_map, map_lock, name, email, fake_url)

def report_listener(people_map, map_lock, shutdown):
    while not shutdown.is_set():
        report_file = receive_new_report(PATH_TO_REPORTS, shutdown) 

        if not report_file:
            continue

        email_and_passwords = xml_to_list(report_file)

        for email, passwords in email_and_passwords.items(): 
            with map_lock:
                if not people_map[email]:
                    people_map[email] = Person("person", email)
                people_map[email].repetitive_password = False
            pass_strength = 0
            for password in passwords:
                with map_lock:
                    if not people_map[email].repetitive_password:
                        people_map[email].repetitive_password = check_common_password(password)
                pass_strength += check_password_strength(password)
                
            # average of password strengths
            pass_strength = pass_strength / len(passwords)

            with map_lock:
                people_map[email].passwords = passwords
                people_map[email].password_score = pass_strength
            
            send_phishing_info_email(people_map[email].name, email, len(people_map[email].passwords), pass_strength)

def save_data_to_file(people_map):
    with open('output/people_data.json', 'w') as f:
        data = {email: {
            'name': person.name,
            'email': email,
            'company': person.company,
            'passwords': person.passwords,
            'password_score': person.password_score,
            'repetitive_password': person.repetitive_password
        } for email, person in people_map.items()}
        json.dump(data, f, indent=2)
    print("[INFO] Data saved to output/people_data.json")

def main():
    fake_url = input("> Enter url to the cloned website: ")

    people_map = {}  # Dictionary to group by email
    map_lock = threading.Lock()
    shutdown = threading.Event()

    t_cmd = threading.Thread(target=user_side, args=(people_map, map_lock, shutdown, fake_url))
    t_rep = threading.Thread(target=report_listener, args=(people_map, map_lock, shutdown))

    t_cmd.start()
    t_rep.start()

    t_cmd.join()
    t_rep.join()

    save_data_to_file(people_map)

if __name__ == "__main__":
    main()