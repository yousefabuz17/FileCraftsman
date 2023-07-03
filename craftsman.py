import os, glob, json, shutil, requests, logging, random
from uuid import uuid4
from pathlib import Path
from bs4 import BeautifulSoup
from links import LINKS
from time import sleep


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
        self.path_name = os.path.join(Path.cwd(), 'FileCraftsman')
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
        file_path = os.path.join(self.json_dir, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    
    def merge_json_files(self):
        all_files = []
        
        def log_path(exception_type):
            errors = {
                FileNotFoundError: ['No JSON files found. Creating new file...', 'Completed'],
                shutil.Error: ['[DATA FOUND] Re-Merging JSON files as \'full_data.json\'...',
                            '*Contents will be different from previous merge*']
            }
            if exception_type in errors:
                logging.error(exception_type)
                for value in errors[exception_type]:
                    sleep(0.5)
                    print(value)
                if exception_type == FileNotFoundError:
                    self.create_directory()
                else:
                    os.remove('full_data.json')
                with open(f'{self.path_name}/full_data.json', 'w') as f3:
                    json.dump(all_files, f3, indent=4)
            return exception_type
        
        try:
            os.chdir(self.json_dir)
            for json_file in glob.glob('*.json'):
                with open(json_file, 'r') as f1:
                    data = json.load(f1)
                all_files.append(data)
                    
            with open(f'{self.path_name}/full_data.json', 'w') as f2:
                json.dump(all_files, f2, indent=4)
            print('Merging JSON files as \'full_data.json\'...')
            sleep(0.5)
            self.move_json_file()
            shutil.rmtree(Path.cwd())
            return all_files

        except (FileNotFoundError, shutil.Error) as e:
            return log_path(type(e))

    
    def move_json_file(self):
        print(f'Moving \'full_data.json\' to parent directory {Path.cwd().name}...')
        sleep(0.5)
        return shutil.move('full_data.json', Path.cwd().parent)


def main():
    links = random.sample(LINKS, 2)

    web_scraper = WebScraper(*links)
    parsed_data = web_scraper.parse_urls()
    if parsed_data:
        json_exporter = JSONExporter('JSON')
        # json_exporter.merge_json_files()  # Merge existing JSON files first
        json_exporter.create_directory()  # Create a new directory for the updated data
        for data in parsed_data:
            json_exporter.export_data(data)
        json_exporter.merge_json_files()  # Merge new JSON files



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()