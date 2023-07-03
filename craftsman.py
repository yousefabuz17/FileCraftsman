import os, sys, glob, json, shutil, requests, logging, random
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
    def __init__(self, json_file_name):
        self.path_name = os.path.join(Path.cwd(), 'FileCraftsman')
        self.json_file_name = json_file_name
        self.json_dir = 'tag_data'
    
    def create_directory(self):
        if not os.path.exists(self.json_dir):
            print(f'Creating temporary directory behind the scenes (\'{self.json_dir}\') to store all parsed links as JSON files')
            os.makedirs(self.json_dir)
    
    def generate_unique_filename(self):
        unique_file_uuid = str(uuid4())[-3:]
        return f'{self.json_dir}{unique_file_uuid}.json'
    
    def export_data(self, data):
        self.create_directory()
        filename = self.generate_unique_filename()
        file_path = os.path.join(self.json_dir, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    
    def merge_json_files(self):
        all_files = []
        try:
            os.chdir(self.json_dir)
            for json_file in glob.glob('*.json'):
                with open(json_file, 'r') as f1:
                    data = json.load(f1)
                all_files.append(data)
                    
            with open(f'{self.json_file_name}.json', 'w') as f2:
                json.dump(all_files, f2, indent=4)
            print(f'Merging all JSON files as \'{self.json_file_name}.json\'')
            self.move_json_file()
            shutil.rmtree(Path.cwd())
            sleep(0.5)
            print('JSON files merged successfully!')
            return all_files

        except (FileNotFoundError, shutil.Error) as e:
            raise e

    def move_json_file(self):
        print(f'Moving the finished \'{self.json_file_name}.json\' to its parent directory')
        sleep(0.5)
        return shutil.move(f'{self.json_file_name}.json', self.path_name)


class LogPathHandler:
    def __init__(self, json_exporter):
        self.json_exporter = json_exporter
    
    def handle_error(self, exception_type):
        errors = {
            FileNotFoundError: ['No JSON files found. Creating new file...', 'JSON files merged successfully!'],
            shutil.Error: ['[DATA FOUND] Restarting the program...',
                           '*Contents will be different from the previous merge*', 'JSON files merged successfully!']
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
            with open(f'{self.json_exporter.json_file_name}.json', 'w') as f1:
                json.dump([], f1, indent=4)
            self.restart_program()
    
    def restart_program(self):
        sleep(0.5)
        python = sys.executable
        os.execl(python, python, *sys.argv)


def main():
    links = random.sample(LINKS, 2)

    web_scraper = WebScraper(*links)
    print('Web scraping activated')
    parsed_data = web_scraper.parse_urls()
    if parsed_data:
        json_exporter = JSONExporter('full_data')
        users_dir_name = json_exporter.json_dir
        json_exporter.create_directory()  # Create a new directory for the updated data
        for data in parsed_data:
            print(f'Parsing URLs, each with its own unique ID: {json_exporter.generate_unique_filename()}')
            json_exporter.export_data(data)
        try:
            json_exporter.merge_json_files()  # Merge new JSON files
        except (FileNotFoundError, shutil.Error) as e:
            log_path_handler = LogPathHandler(json_exporter)
            log_path_handler.handle_error(type(e))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
