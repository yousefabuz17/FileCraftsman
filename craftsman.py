import os, requests, json
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
    
    def get_p_contents(self):
        contents_ = []
        for i in self.url:
            response = requests.get(i).text
            soup = BeautifulSoup(response, 'html.parser').find_all('p')
            for j in soup:
                contents_.append(j.text.split())
        full_contents = ''.join([' '.join(i) for i in contents_])
        return self.add_word_count(full_contents)
    
    def add_word_count(self, words):
        return f"{words}\n\n\033[1;4;33:47mWordCount:\033[0m {words.__len__()}"

w = WebScraper('https://www.cs.cmu.edu/~bingbin/', 'https://www.gutenberg.org/cache/epub/71080/pg71080-images.html', 'https://www.sciencedirect.com/topics/computer-science/research-paper').get_p_contents()


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
