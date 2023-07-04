import os
import sys
import glob
import json
import shutil
import logging
import random
from uuid import uuid4
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from time import sleep
from links import LINKS

class WebScraper:
    def __init__(self, urls=None, limit=None):
        logging.info('Web scraping activated')
        self.urls = self._limit_urls(urls, limit)

    def _limit_urls(self, urls, limit):
        if urls is not None:
            urls = random.sample(urls, min(limit, len(urls))) if limit else urls
        else:
            urls = random.sample(LINKS, 5) if limit is None else random.sample(LINKS, limit)
        return urls

    def get_tag_info(self, soup):
        all_tags = soup.find_all(True)
        tag_info = {
            'tag_names': list(set(tag.name for tag in all_tags)),
            'tag_attr': [tag.attrs for tag in all_tags if tag.attrs],
            'tag_text': [tag.text for tag in all_tags if tag.text],
            'tag_contents': [list(filter(lambda content: content, [sub_tag.text for sub_tag in tag.contents if sub_tag.text])) for tag in all_tags]
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
    def __init__(self, json_file_name='full_data'):
        self.path_name = os.path.join(Path.cwd(), 'FileCraftsman')
        self.json_file_name = json_file_name
        self.json_dir = 'TempJSONFiles'
        self.create_directory()

    def create_directory(self):
        os.makedirs(self.json_dir, exist_ok=True)
        print(f'Created temporary directory: {self.json_dir} to store parsed links as JSON files')

    def generate_unique_filename(self):
        unique_file_uuid = str(uuid4())[-3:]
        file_name = f'{self.json_dir}_{unique_file_uuid}.json'
        return file_name

    def export_data(self, data):
        filename = self.generate_unique_filename()
        file_path = os.path.join(self.json_dir, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def merge_json_files(self):
        all_files = []
        os.chdir(self.json_dir)
        for json_file in glob.glob('*.json'):
            with open(json_file, 'r') as f1:
                data = json.load(f1)
            all_files.append(data)

        with open(f'{self.json_file_name}.json', 'w') as f2:
            json.dump(all_files, f2, indent=4)
        print(f'Merged all JSON files as {self.json_file_name}.json')
        self.move_json_file()
        shutil.rmtree(Path.cwd())
        self.completed()
        return all_files

    def move_json_file(self):
        print(f'Moving finished JSON file to parent directory: {self.path_name}')
        sleep(0.5)
        file_name = f'{self.json_file_name}.json'
        shutil.move(file_name, self.path_name)

    def completed(self):
        full_path = os.path.join(self.path_name, f'{self.json_file_name}.json')
        print(f'JSON files merged successfully!\n{self.json_file_name}.json saved at: {full_path}')
        sleep(0.5)

class LogPathHandler:
    def __init__(self, json_exporter):
        self.json_exporter = json_exporter
    
    def handle_error(self, exception_type):
        errors = {
            FileNotFoundError: ['No JSON files found. Creating new file...'],
            shutil.Error: [
                        '[DATA FOUND] File already exists in the parent directory.',
                        'Restarting the program... Please wait',
                        'Deleting the old file...',
                        '*Contents will be different from the previous merge*',
                        'File name will be changed to its parents directory name',
                        'Restarting the program... Please wait',
                        'Program successfully restarted!']
        }
        if exception_type in errors:
            logging.error(exception_type)
            for value in errors[exception_type]:
                sleep(0.2)
                print(value)
            if exception_type == FileNotFoundError:
                self.json_exporter.create_directory()
            else:
                os.remove(f'{self.json_exporter.json_file_name}.json')
            self.restart_program(f'{self.json_exporter.json_file_name}')
    
    def restart_program(self, file):
        print(os.getcwd())
        file_name = f'{file}.json'
        os.chdir('../FileCraftsman')
        os.remove(file_name)
        sleep(0.5)
        main()

def main():
    logging.basicConfig(level=logging.INFO)
    web_scraper = WebScraper(limit=2)
    parsed_data = web_scraper.parse_urls()
    if parsed_data:
        json_exporter = JSONExporter()
        unique_filename = json_exporter.generate_unique_filename()
        for data in parsed_data:
            print(f'Parsing URLs with unique ID: {unique_filename}')
            json_exporter.export_data(data)
        try:
            json_exporter.merge_json_files()
        except (FileNotFoundError, shutil.Error) as e:
            LogPathHandler(json_exporter).handle_error(type(e))

if __name__ == "__main__":
    main()
