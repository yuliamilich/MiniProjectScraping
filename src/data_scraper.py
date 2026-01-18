import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# find and write into search bar
def type_searchbar(wait, name):
    search_box = wait.until(
        EC.element_to_be_clickable((By.ID, "global-search"))
    )
    search_box.clear()
    search_box.send_keys(name)
    time.sleep(0.5)
    search_box.send_keys(Keys.BACKSPACE)
    search_box.send_keys(name[-1])

# find first option from drop menu
def click_first_result(wait):
    first_result = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#search-results > div")
        )
    )
    first_result.click()

# wait for page to get populated 
def load_profile_page(wait, name):
    result_name = wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "profile-name"), name
        )
    )

# Now elements are populated
def fetch_work_or_school(driver):
    work = driver.find_element(By.ID, "profile-work").text

    if work=="None" or work == "":
        school = driver.find_element(By.ID, "profile-school").text
        return school if school and school != "None" else None
    else:
        return work


def get_company(person_name):
    if not person_name or person_name.strip() == "":
        print("Error: Name cannot be empty")
        return None

    driver = webdriver.Chrome() 

    wait = WebDriverWait(driver, 10)

    driver.get("http://localhost:8000")

    type_searchbar(wait, person_name)
    click_first_result(wait)
    load_profile_page(wait, person_name)
    company = fetch_work_or_school(driver)

    driver.quit()

    if not company:
        print(f"Warning: No company or school information found for {person_name}")
        return None
    
    print(company)
    return company