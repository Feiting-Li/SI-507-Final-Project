import os
import time
import csv
from datetime import datetime
from bs4 import BeautifulSoup
import questionary
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Node:
    def __init__(self, data):
        """
        Initializes a new node with the given data.

        Attributes
        ----------
        data : Any
            The data stored in the node.
        next : Node or None
            The next node in the linked list.
        Parameters
        ----------
        data : Any, optional
            The data to be stored in the node (default is None).
        """
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        """
        Initializes a new empty linked list.
        """
        self.head = None
    
    def append(self, data):
        """
        Appends a new node with the specified data to the end of the list.

        :param data: The data to append to the list.
        """
        if not self.head:
            self.head = Node(data)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(data)
    
    def to_list(self):
        """
        Converts the linked list to a Python list of data.

        :return: A list containing all data elements from the linked list.
        """
        data = []
        current = self.head
        while current:
            data.append(current.data)
            current = current.next
        return data
    
    def find(self, name):
        """
        Finds the first node with the specified name in the list.

        :param name: The name to search for within the node data.
        :return: The node data if found, otherwise None.
        """
        current = self.head
        while current:
            if current.data['name'] == name:
                return current.data
            current = current.next
        return None

def auto_click_more(driver, click_count):
    """
    Automatically clicks a "Load more" button on a webpage for a given number of times.

    :param driver: The Selenium WebDriver instance to interact with the browser.
    :param click_count: Number of times the "Load more" button needs to be clicked.
    """
    scroll_pause_time = 2
    total_height = driver.execute_script("return document.body.scrollHeight")
    button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Load more']"))
    )
    for _ in range(click_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        if button.is_displayed():
            button.click()
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == total_height:
            break
        total_height = new_height

def scrape_data():
    """
    Scrapes data from a web page using Selenium WebDriver.

    :return: A LinkedList instance containing scraped data.
    """
    options = {
        "5": 5,
        "10": 10,
        "20": 20,
        "30": 25,
    }
    selected = questionary.select(
        "Please select the number of data pages you want to obtain:", options
    ).ask()
    driver = webdriver.Firefox()
    driver.get("https://www.nbatopshot.com/search?")
    data_list = LinkedList()
    try:
        time.sleep(20)
        auto_click_more(driver, int(selected))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        
        for block in soup.select(".css-1850lbl > div"):
            data = {
                "link": f"https://www.nbatopshot.com{block.select_one('.chakra-linkbox__overlay').get('href')}" if block.select_one('.chakra-linkbox__overlay') else None,
                "common": block.select_one('.css-1kgpxnt').get_text() if block.select_one('.css-1kgpxnt') else None,
                "name": block.select_one('.chakra-heading').get_text() if block.select_one('.chakra-heading') else None,
                "lowest_ask": block.select_one('.css-1hwxzsy').get_text() if block.select_one('.css-1hwxzsy') else None,
                "avg_sale": block.select_one('.css-zv2k34').get_text() if block.select_one('.css-zv2k34') else None,
                "hook_shot": block.select_one('.css-17udwdn').get_text() if block.select_one('.css-17udwdn') else None
            }
            data_list.append(data)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
    return data_list

def player_list(data_list):
    """
    Return a list with players name scraped from the web page

    :param data_list: A LinkedList instance containing scraped data.
    :return: A list with players name
    """
    players = []
    current = data_list.head
    while current:
        players.append(current.data['name'])
        current = current.next
    return list(set(players))

def choose_name(name, data_list):
    """
    Return a list of lists with information of NFTs of the player users input

    :param name: The player's name users input
    :param data_list: A LinkedList instance containing scraped data.
    :return: A list of dictionaries which are the information of NFTs of the player users input
    """
    return [data for data in data_list.to_list() if data['name'] == name]


def write_csv(data_list):
    data = data_list if isinstance(data_list, list) else data_list.to_list()
    current_date = datetime.now()
    formatted_date = current_date.strftime("%m%d%Y")
    WORKPATH = os.getcwd()
    CSVPATH = f"{WORKPATH}/topshot_data_{formatted_date}.csv"
    with open(CSVPATH, "w", newline="", encoding="utf-8") as w:
        # writer = csv.writer(w)
        # writer.writerow(["link", "common", "name", "lowest_ask", "avg_sale", "hook_shot"])
        # writer.writerows(data)
        writer = csv.DictWriter(w, fieldnames=["link", "common", "name", "lowest_ask", "avg_sale", "hook_shot"])
        writer.writeheader()
        writer.writerows(data)
        print(f"{len(data)} items of data have been saved, and the file path is: {CSVPATH}")


def main():
    data = scrape_data()
    name = player_list(data)
    print(f"Here are the players we collected: {name}")
    while True:
        try:
            player = input("Which players or teams you are looking for from the list above)")

        except ValueError:
            print("That isn't a valid name. Try it again?")
            continue
        else:
            if player in name:
                print(f"Here are the data about {player}: {choose_name(player,data)}")
                write_csv(choose_name(player,data))
                break
            else:
                print("That isn't a valid place. Try another NAME!")       
    

if __name__ == "__main__":
    main()
