import os
import requests
import json
import glob
import re
from pathlib import Path
from bs4 import BeautifulSoup
from uuid import uuid4


class WebScraper:
    def __init__(self, *url):
        self.url = list(url)
        self.arg_length = self.url.__len__()
        self.path_name = Path.cwd().name
    
    def get_url_id(self, index):
        all_links = {key: value for key, value in enumerate(self.url)}
        return all_links.get(index)
    
    def parse_url(self):
        all_tags = []
        for urls in self.url:
            response = requests.get(urls).text
            soup = BeautifulSoup(response, 'html.parser')
            tags = self.get_tag_info(soup)
            all_tags.append(tags)
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
        json_dir = 'JSON'
        unique_file_uuid = str(uuid4())[-3:]
        org_file_name = f'{json_dir}/tag_data.json'
        new_file_name = f'{json_dir}/tag_data{unique_file_uuid}.json'
        if not os.path.exists('JSON'):
            os.makedirs('JSON')
        if not os.path.exists(org_file_name):
            with open(org_file_name, 'w') as file:
                json.dump(data, file, indent=4)
        else:
            with open(new_file_name, 'w') as file:
                json.dump(data, file, indent=4)

class CleanData:
    def __init__(self, directory=None):
        self.directory = directory
    
    def all_json_files(self):
        os.chdir('JSON')
        return glob.glob('*.json')


def main():
    links = ('https://www.youtube.com/', 'https://www.cs.cmu.edu/~bingbin/', 'https://www.gutenberg.org/cache/epub/71080/pg71080-images.html', 'https://www.sciencedirect.com/topics/computer-science/research-paper', 'https://www.linkedin.com/')

    if links:
        web_link_parser = WebScraper(*links)
        parsed_data = web_link_parser.parse_url()
        if parsed_data:
            web_link_parser.export_tag_data(parsed_data) #Exports data into JSON folder
            data = CleanData()
            json_files = data.all_json_files()
        else:
            print("Error: No tag information found")
    else:
        print('Error: No links were provided')

main()
