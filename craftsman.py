import os, requests, json
import re
from subprocess import call
from pathlib import Path
from bs4 import BeautifulSoup
from pprint import pprint
from uuid import uuid4


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
        tag_info = {
            'tag_names': list(set(i.name for i in all_tags)),
            'tag_attr': [i.attrs for i in all_tags if i.attrs],
            'tag_text': [i.text for i in all_tags if i.text],
            'tag_contents': list(filter(lambda k: k,[[j.text for j in tag.contents if j.text] for tag in all_tags]))
        }
        self.export_tag_data(tag_info)
        return tag_info
    
    def export_tag_data(self, data):
        unique_file_uuid = str(uuid4())[-3:]
        file_name = f'FileCraftsman/tag_data{unique_file_uuid}.json'
        if not os.path.exists('FileCraftsman/tag_data.json'):
            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)
                file.close()
                CleanData(file_name).merge_tag_data()

class CleanData:
    def __init__(self, file_name):
        self.file_name = file_name

    def merge_tag_data(self):
        merged_data = {}
        
        with open(self.file_name, 'r') as file1:
            data = json.load(file1)
        
        for key, value in data.items():
            if key in merged_data:
                data[key].extend(value)
            else:
                merged_data[key] = value
        
        with open(self.file_name, 'w') as f:
            json.dump(merged_data, f, indent=4)
            f.close()


class RemoveFiles:
    def __init__(self):
        self.files = os.listdir()
        self.cwd, self.path_name = Path.cwd(), Path.cwd().name
    
    def fetch_all_files(self):
        if self.cwd == self.path_name:
            tag_files = [i for i in self.files if i.startswith('tag_data')]
        elif self.cwd != self.path_name:
            os.chdir('FileCraftsman')
            tag_files = [i for i in self.files if i.startswith('tag_data')]
        return tag_files
    
    # def remove(self):
    #     if self.cwd == self.path_name:
    #         all_files = self.fetch_all_files()
    #         print(max(all_files))
    #     elif self.cwd != self.path_name:
    #         os.chdir('FileCraftsman')
    #         all_files = self.fetch_all_files()
    #         print(all_files)


links = 'https://www.youtube.com/','https://www.cs.cmu.edu/~bingbin/','https://www.gutenberg.org/cache/epub/71080/pg71080-images.html','https://www.sciencedirect.com/topics/computer-science/research-paper','https://www.linkedin.com/'
#,'https://www.cs.cmu.edu/~bingbin/','https://www.gutenberg.org/cache/epub/71080/pg71080-images.html','https://www.sciencedirect.com/topics/computer-science/research-paper','https://www.linkedin.com/'
# w = WebScraper(*links).get_all_contents()
w = WebScraper(*links).parse_url()
print(RemoveFiles().fetch_all_files())




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
