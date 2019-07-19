from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import NavigableString

# Chrome Options:
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# Data Definitions:
eccolaide_website = "https://mbcet.ecoleaide.com/home.htm"
attendance_url = "https://mbcet.ecoleaide.com/search/subjAttendReport.htm"
username = "*SNIP*"
password = "*SNIP*"
start_date = "01/01/2018"

# Parsed Data:
subject_list = list()
total_hours = list()
present_hours = list()
attendance_percentage = list()


def get_attendance_source():

    browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
    browser.get(eccolaide_website)
    # Input the login credentials
    user_field = browser.find_element_by_id("username_temp")
    pass_field = browser.find_element_by_id("form-password")
    login_button = browser.find_elements_by_xpath("//*[contains(text(), 'Sign in')]")
    user_field.send_keys(username)
    pass_field.send_keys(password)
    # Note : login_button is a list of elements containing 'Sign in'
    login_button[0].click()
    browser.get(attendance_url)
    from_date = browser.find_element_by_id("form1_fromDate")
    # Don't blame the code , blame the badly written website.
    from_date.send_keys(Keys.CONTROL + "a")
    from_date.send_keys(Keys.DELETE)
    from_date.send_keys(start_date)
    from_date.clear()
    from_date.send_keys(start_date)
    attendance_submit_button = browser.find_element_by_id("form1_generate")
    attendance_submit_button.click()
    source = browser.page_source
    browser.quit()
    return source


def parse_attendance_source():
    main_source = get_attendance_source()
    soup = BeautifulSoup(main_source)
    string_list = list()

    # Find the elements containing tr
    tr = soup.find_all('tr')

    # Find all the NavigableString and delete them
    for x in range(0, len(tr)):
        if isinstance(tr[x], NavigableString):
            del tr[x]

    # Remove the headings of the table , we wont need them.
    tr = tr[1:]
    # Iterate through the rows and extract all the strings inside
    for x in tr:
        for string in x.stripped_strings:
            string_list.append(string)

    # Lets abstract the data into corresponding lists
    for x in range(0, len(string_list), 3):
        subject_list.append(string_list[x])
        total_hours.append(string_list[x + 1])
        present_hours.append(string_list[x + 2])
    # Printing the data
    for x in range(0, len(subject_list)):
        attendance_percentage.append(float(present_hours[x]) / float(total_hours[x]) * 100.0)
        print subject_list[x], ":", total_hours[x], ":", present_hours[x], ":", attendance_percentage[x], "%"


def main_entrypoint():
    parse_attendance_source()


if __name__ == '__main__':
    main_entrypoint()
