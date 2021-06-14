from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://bbs-simulator.com/story"
driver.get(url)
delay = 2  # in seconds
try:
    myElem = WebDriverWait(driver, delay).until(expected_conditions.presence_of_element_located((By.ID, 'storyTabSearch5')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

source = driver.page_source
soup = BeautifulSoup(source, "html.parser")

orb_information = dict()


def is_invalid_name(name):
    return name == 'Rewards' or name == 'Drops' or name == 'Bonus Units' or name == 'Requires'


def parse_story_name(information_div, category_name):
    """
    Parses the story name from the given information_div and assigns it to a dictionary with the category_name.
    :param information_div: div where the story name is held
    :param category_name: category of the story
    :return: None
    """
    index = 0
    for name in information_div.findChildren('b'):
        name_text = name.text.replace('<b>', '').replace('</b>', '')
        if not is_invalid_name(name_text) and not None:
            orb_information[category_name][index] = [name_text, -1]
            index = index + 1


def parse_orb_count(information_div, category_name):
    """
    Parses the orb count from the information_div by searching for the image of it.
    :param information_div: div where the story name is held
    :param category_name: category of the story
    :return: None
    """
    index = 0
    for orb_info in information_div.find_all("img", {
        "src": "https://bucket.bbs-simulator.com/item/0017-ce1df5d4-c569-4794-b260-3a39d5e13891.png"}):
        if orb_info is not None:
            orb_count = int(orb_info.parent.span.text)
            orb_information[category_name][index][1] = orb_count
            index = index + 1


def parse_category_name(category_div):
    """
    Parses the div where the category name is located and assigns it to the dictionary orb_information.
    :param category_div: div where category name is located
    :return: None
    """
    name_holder = category_div.div.div.input
    if name_holder is None or name_holder.has_attr('aria-label') is None:
        return "Error. Name not found."

    cat_name = (str(name_holder.attrs['aria-label']).replace(" name", ""))
    orb_information[cat_name] = {}
    return cat_name


def parse_website():
    """
    Parses the website for story and orb information.
    :return: None
    """
    print(f"Parsing {url} for orb information\n")
    tab_content_div = soup.find("div", {"class": "tab-content"})
    tab_content_div: Tag
    for tab_panel_div in tab_content_div:
        category_div = tab_panel_div.find("div", {"class": "row"})
        category_name = parse_category_name(category_div)  # name of the category

        # div where story name and orb count is located
        information_div = tab_panel_div.find("div", {"class": "w-100 card-body"})

        parse_story_name(information_div, category_name)  # story name
        parse_orb_count(information_div, category_name)  # orb count


def print_information():
    """
    Prints out orb_information dictionary for easier readability.
    :return: None
    """
    story_orb_totals_lst = [0] * 6
    index = 0
    for category_type_key, category_type_value in orb_information.items():
        print(category_type_key, '\n')
        for story_key, orb_info_key in category_type_value.items():
            story_name = orb_info_key[0]
            orb_count = orb_info_key[1]
            print(story_name, "'s Orb Count: ", orb_count)
            story_orb_totals_lst[index] = story_orb_totals_lst[index] + orb_count
        print()
        print(category_type_key, "'s Total Orb Count: ", story_orb_totals_lst[index], '\n\n')
        index = index + 1

    print("Total Orb Count: ", sum(story_orb_totals_lst))


def main():
    try:
        parse_website()
        print_information()
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
