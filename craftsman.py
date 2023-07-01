import os, requests, json
from subprocess import call
from pathlib import Path
from bs4 import BeautifulSoup
from pprint import pprint

# Class for webscraping
#   This class will be used to scrape stories and random information from the web
#   to be added into text files to be manipulated and practiced with
    # 1. Method to request & parse contents from different webpages
    # 2. Method to retrieve random information from webpages
    # 3. Method to merge all contents into an organized json file
    # 4. Get method to retrieve contents from json file
    # 5. Links to parse from:
            # https://www.cs.cmu.edu/~bingbin/
            # https://www.gutenberg.org/cache/epub/71080/pg71080-images.html
            # https://www.sciencedirect.com/topics/computer-science/research-paper
class WebScraper:
    def __init__(self, *url):
        self.url = list(url)
        self.all_contents = {}
    
    def get_first_contents(self):
        contents_ = []
        for _, element in enumerate(self.url[:3]):
            first_response = requests.get(element).text
            soup = BeautifulSoup(first_response, 'html.parser')
            try:
                p_contents = soup.find_all('p')
                img_contents = soup.find_all('img')
                both_contents = p_contents + img_contents
            except AttributeError: continue
            for j in both_contents:
                contents_.append(j.text.split())
        full_contents = self.add_word_count(''.join([' '.join(c) for c in contents_]))
        self.all_contents['first_contents'] = full_contents
        return full_contents
    
    def get_second_contents(self):
        contents_ = []
        for _, element in enumerate(self.url[3:]):
            second_response = requests.get(element).text
            soup = BeautifulSoup(second_response, 'html.parser')
            try:
                li_contents = soup.find_all('li', class_='toctree-l2')
                href_contents = soup.find_all('a', class_='reference internal')
                for li in li_contents:
                    contents_.append(li.text)
                for href in href_contents:
                    contents_.append(href.text)
            except AttributeError: continue
        full_contents = self.add_word_count(''.join([''.join(c) for c in contents_]))
        self.all_contents['second_contents'] = contents_
        return full_contents
            
    
    def add_word_count(self, words):
        return f"{words}\n\n\033[1;4;33:47mWord Count:\033[0m {words.__len__()}"


links = 'https://www.cs.cmu.edu/~bingbin/', 'https://www.gutenberg.org/cache/epub/71080/pg71080-images.html', 'https://www.sciencedirect.com/topics/computer-science/research-paper', 'https://docs.python.org/3/library/'

w = WebScraper(*links).get_first_contents()


print(w)



# Class for Craftsman
#   This class will be used to create random directories and text files
#   to be used for practicing and learning
    # 1. Method to check current directory
        # 1a. If current directory is not Desktop, change to Desktop
        # 1b. If current directory is Desktop, make the first testing directory
    # 2. Method to create a specific set of numbered directories
    # 3. Method to create a specific set of numbered text files
        # 3a. Change to be set based on user input instead of hard coded
    # 4. Method to create the directories first, then generate the text files
        # 4a. Fetch the generated information from the webscraper class to be added onto the text files
