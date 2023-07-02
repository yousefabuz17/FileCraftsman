import os
import requests
import json
import glob
from pathlib import Path
from bs4 import BeautifulSoup
from uuid import uuid4
import logging


class WebScraper:
    def __init__(self, *urls):
        self.urls = list(urls)
    
    def get_tag_info(self, soup):
        all_tags = soup.find_all(True)
        tag_info = {
            'tag_names': list(set(i.name for i in all_tags)),
            'tag_attr': [i.attrs for i in all_tags if i.attrs],
            'tag_text': [i.text for i in all_tags if i.text],
            'tag_contents': list(filter(lambda k: k,[[j.text for j in tag.contents if j.text] for tag in all_tags]))
        }
        return tag_info
    
    def parse_url(self, url):
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        return self.get_tag_info(soup)
    
    def parse_urls(self):
        all_tags = []
        for url in self.urls:
            tags = self.parse_url(url)
            all_tags.append(tags)
        return all_tags


class JSONExporter:
    def __init__(self, directory):
        self.directory = directory
        self.json_dir = 'JSON'
    
    def create_directory(self):
        if not os.path.exists(self.json_dir):
            os.makedirs(self.json_dir)
    
    def generate_unique_filename(self):
        unique_file_uuid = str(uuid4())[-3:]
        return f'tag_data{unique_file_uuid}.json'
    
    def export_data(self, data):
        self.create_directory()
        filename = self.generate_unique_filename()
        file_path = os.path.join(self.directory, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    
    def merge_json_files(self):
        all_files = []
        os.chdir(self.directory)
        for json_file in glob.glob('*.json'):
            with open(json_file, 'r') as file:
                data = json.load(file)
            all_files.append(data)
            
            with open('full_data.json', 'w') as file:
                json.dump(all_files, file, indent=4)

        return all_files


def main():
    links = ('https://www.youtube.com/', 'https://www.cs.cmu.edu/~bingbin/', 'https://www.gutenberg.org/cache/epub/71080/pg71080-images.html', 'https://www.sciencedirect.com/topics/computer-science/research-paper', 'https://www.linkedin.com/')

    if links:
        web_scraper = WebScraper(*links)
        parsed_data = web_scraper.parse_urls()
        if parsed_data:
            json_exporter = JSONExporter('JSON')
            for data in parsed_data:
                json_exporter.export_data(data)
            json_full_data = json_exporter.merge_json_files()
            print(json_full_data)
        else:
            print("Error: No tag information found")
    else:
        print('Error: No links were provided')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
