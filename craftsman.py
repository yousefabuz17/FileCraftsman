import os, requests, json
import re
from subprocess import call
from pathlib import Path
from bs4 import BeautifulSoup
from pprint import pprint


class WebScraper:
    def __init__(self, *url):
        self.url = list(url)
        self.all_contents = {}
        self.arg_length = self.url.__len__()
    
    def parse_url(self):
        for urls in self.url:
            response = requests.get(urls).text
            soup = BeautifulSoup(response, 'html.parser')
            all_tags = self.get_tag_info(soup)
        return all_tags
    
    def get_tag_info(self, soup):
        all_tags = soup.find_all(True)
        for i in all_tags:
            tag_info = {
                'tag_names': [i.name for tag in all_tags],
                'tag_attr': [i.attrs for tag in all_tags],
                'tag_text': [i.text for tag in all_tags],
                'tag_contents': [[i.string for i in tag.contents] for tag in all_tags],
                'tag_parent': [],
                'tag_children': [],  
                'tag_descendants': [],
                'tag_next_sibling': [],
                'tag_previous_sibling': [],
                'tag_next_siblings': []
            }
            if not os.path.exists('FileCraftsman/tag_data.json'):
                with open('FileCraftsman/tag_data.json', 'w') as file:
                    json.dump(tag_info, file, indent=4)
        return tag_info
    #     return self.tag_to_json(tag_info)
    
    # def tag_to_json(self, tag_info):
    #     if not os.path.exists('FileCraftsman/tag_data.json'):
    #         with open('FileCraftsman/tag_data.json', 'w') as file:
    #             json.dump(tag_info, file, indent=4)

    
    # def one_link(self):
    #     # contents_ = []
    #     response = requests.get(self.url[0]).text
    #     soup = BeautifulSoup(response, 'html.parser')
    #     all_tags = soup.find_all(True)
    #     try:
    #         tag_names = [tag.name for tag in all_tags]
    #         tag_attr = [tag.attrs for tag in all_tags]
    #     except AttributeError: return "Invalid"
    #     # self.all_contents['one_link'] = self.add_word_count(''.join([''.join(c) for c in contents_]))
    #     self.all_contents['one_link'] = all_tags
    #     return all_tags
    #     #FIND A WAY TO USE REGEX TO REMOVE IP ADDRESSES AND EMAILS
    
    # def get_first_contents(self):
    #     contents_ = []
    #     for _, element in enumerate(self.url[:(self.arg_length//2)+1]):
    #         first_response = requests.get(element).text
    #         soup = BeautifulSoup(first_response, 'html.parser')
    #         try:
    #             p_contents = soup.find_all('p')
    #             img_contents = soup.find_all('img')
    #             both_contents = p_contents + img_contents
    #         except AttributeError: continue
    #         for j in both_contents:
    #             contents_.append(j.text.split())
    #     full_contents = self.add_word_count(''.join([' '.join(c) for c in contents_]))
    #     return full_contents
    
    # def get_second_contents(self):
    #     contents_ = []
    #     for _, element in enumerate(self.url[(self.arg_length//2):]):
    #         second_response = requests.get(element).text
    #         soup = BeautifulSoup(second_response, 'html.parser')
    #         try:
    #             li_contents = soup.find_all('li', class_='toctree-l2')
    #             href_contents = soup.find_all('a', class_='reference internal')
    #             p_contents = soup.find_all('p')
    #             for content in li_contents+href_contents+p_contents:
    #                 contents_.append(content.text)
    #         except AttributeError: continue
    #     full_contents = self.add_word_count(''.join([''.join(c) for c in contents_]))
    #     return full_contents
    
    # def add_word_count(self, words):
    #     return f"{words}\n\n\033[1;4;33:47mWord Count:\033[0m {words.__len__()}"
    
    # def merged_contents(self):
    #     self.all_contents['first_contents'] = self.get_first_contents()
    #     self.all_contents['second_contents'] = self.get_second_contents()
    #     self.data_to_json()
    #     return self.all_contents
    
    # def get_all_contents(self):
    #     try:
    #         if self.arg_length == 1:
    #             self.one_link()
    #             return self.get_contents()
    #         return self.merged_contents()
    #     except requests.exceptions.InvalidSchema:
    #         return f'Invalid: {self.url} cannot be fetched.'
    
    # def get_contents(self):
    #     self.data_to_json()
    #     return self.all_contents
    
    # def data_to_json(self):
    #     new_data = {
    #         'one_link': self.all_contents.get('one_link', None),
    #         'first_contents': self.all_contents.get('first_contents', None),
    #         'second_contents': self.all_contents.get('second_contents', None)
    #     }
    #     with open('FileCraftsman/contents.json', 'w') as file:
    #         json.dump(new_data, file, indent=4)


links = 'https://www.youtube.com/',
#,'https://www.cs.cmu.edu/~bingbin/','https://www.gutenberg.org/cache/epub/71080/pg71080-images.html','https://www.sciencedirect.com/topics/computer-science/research-paper','https://www.linkedin.com/'
# w = WebScraper(*links).get_all_contents()
w = WebScraper(*links).parse_url()





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
