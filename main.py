from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

url = 'https://bbs-simulator.com/story'
chromedriver_path = './chromedriver/chromedriver.exe'
orb_img_path = "https://bucket.bbs-simulator.com/item/0017-ce1df5d4-c569-4794-b260-3a39d5e13891.png"

driver = webdriver.Chrome(chromedriver_path)
driver.get(url)
delay = 2  # in seconds
try:
    myElem = WebDriverWait(driver, delay).until(
        expected_conditions.presence_of_element_located((By.ID, 'storyTabSearch5')))
    print("Page loaded successfully.")
except TimeoutException:
    print(f"Page loading took too long.")

soup = BeautifulSoup(driver.page_source, "html.parser")

orb_information = dict()


def is_invalid_name(name):
    return name == 'Rewards' or name == 'Drops' or name == 'Bonus Units' or name == 'Requires'


def parse_story_name(card_body, category_name, card_length):
    """
    Parses the story name from the given card_body and assigns it to a dictionary with the category name.
    :param card_body: div where the story name is held
    :param category_name: category of the story
    :param card_length: length of cards to parse
    :return: None
    """
    index = card_length if (card_length > 0) else 0
    for name in card_body.findChildren('b'):
        name_text: str = name.text.replace('<b>', '').replace('</b>', '')
        if not is_invalid_name(name_text) and not None:
            orb_information[category_name][index] = [name_text, 0]
            index = index + 1


def parse_orb_count(card_body, category_name, card_length):
    """
    Parses the orb count from the card_body by searching for the image of it.
    :param card_body: div where the story name is held
    :param category_name: category of the story
    :param card_length: length of cards to parse
    :return: None
    """
    index = card_length if (card_length > 0) else 0
    for orb_info in card_body.find_all("img", {
        "src": orb_img_path}):
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

    category_name = (str(name_holder.attrs['aria-label']).replace(" name", ""))
    orb_information[category_name] = {}
    return category_name


def change_story_tab(tab_index):
    """
    Changes the page focus to a new story tab based on the input index and updates the soup object.
    :param tab_index: story tab index
    :return: None
    """
    global soup
    driver.find_element_by_xpath(f"//a[@data-rb-event-key='storyTab{tab_index}']").click()

    # Update the soup object so Selenium can see the new elements
    soup = BeautifulSoup(driver.page_source, "html.parser")


def get_tab_panel():
    tab_content_div = soup.find("div", {"class": "tab-content"})
    tab_page_div = tab_content_div.find("div", {"class": "fade nav-tabs-dark tab-pane active show"})
    return tab_page_div


def get_card_length(card_body):
    for child in card_body.findChildren():
        if "Showing 1-" in child.text:
            return int(child.text.split()[-1])
    return 0


def get_story_tab_count():
    return len(soup.find("nav", {"class": "nav-tabs-dark nav nav-tabs nav-fill"}))


def parse_story():
    """
    Parses the website for story orb information.
    :return: None
    """
    print(f"Parsing {url} for orb information\n")

    story_tab_count = get_story_tab_count()

    for index in range(0, story_tab_count):
        if index > 0:
            change_story_tab(index)
        tab_panel_div = get_tab_panel()
        if tab_panel_div is None:
            return
        category_div = tab_panel_div.find("div", {"class": "row"})
        category_name = parse_category_name(category_div)

        card_body = tab_panel_div.find("div", {"class": "w-100 card-body"})
        total_card_length = get_card_length(card_body)

        parse_tab(index, category_name, card_body, total_card_length)


def print_information():
    """
    Prints out orb_information dictionary.
    :return: None
    """
    story_orb_totals_lst = [0] * get_story_tab_count()
    index = 0
    for category_type_key, category_type_value in orb_information.items():
        print(category_type_key, '\n')
        for story_key, orb_info_key in category_type_value.items():
            story_name = orb_info_key[0].encode('ascii', 'ignore').decode('ascii')
            orb_count = orb_info_key[1]
            print(story_name, "Orb Count: ", orb_count)
            story_orb_totals_lst[index] = story_orb_totals_lst[index] + orb_count
        print()
        print(category_type_key, "Total Orb Count: ", story_orb_totals_lst[index], '\n\n')
        index = index + 1

    print("Total Orb Count: ", sum(story_orb_totals_lst))


def click_next_page(btn_index):
    global soup
    next_btn = driver.find_elements_by_xpath('//*[text() = ">"]')[btn_index * 2]
    next_btn.click()
    soup = BeautifulSoup(driver.page_source, "html.parser")


def parse_tab(index, category_name, card_body, total_card_length, new_card_index=0):
    """
      Parses the visible tab, a bunch of cards in the card body.
      :return: None
      """
    if total_card_length == new_card_index:
        return
    visible_card_length = len(card_body.find_all("div", {"class": "card"}, recursive=False))

    parse_story_name(card_body, category_name, new_card_index)
    parse_orb_count(card_body, category_name, new_card_index)

    click_next_page(index)
    tab_panel_div = get_tab_panel()
    card_body = tab_panel_div.find("div", {"class": "w-100 card-body"})

    parse_tab(index, category_name, card_body, total_card_length,
              new_card_index + visible_card_length)


def main():
    try:
        parse_story()
        print_information()
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
