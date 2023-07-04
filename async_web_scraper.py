import json
import shutil
import random
import logging
import aiohttp
import asyncio
from uuid import uuid4
from pathlib import Path
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from links import LINKS

class AsyncWebScraper:
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

    async def parse_url(self, url, session):
        async with session.get(url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            return self.get_tag_info(soup)

    async def parse_urls(self):
        all_tags = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.parse_url(url, session) for url in self.urls]
            all_tags = await asyncio.gather(*tasks)
        return all_tags


class JSONExporter:
    def __init__(self, json_file_name='full_data'):
        self.path_name = Path.cwd() / 'FileCraftsman'
        self.json_file_name = json_file_name
        self.json_dir = Path('TempJSONFiles')
        self.json_dir.mkdir(exist_ok=True)
        print(f'Created temporary directory: {self.json_dir} to store parsed links as JSON files')

    def generate_unique_filename(self):
        unique_file_uuid = str(uuid4())[-3:]
        file_name = f'{self.json_dir}_{unique_file_uuid}.json'
        return file_name

    def export_data(self, data):
        filename = self.generate_unique_filename()
        file_path = self.json_dir / filename
        with file_path.open('w') as file:
            json.dump(data, file, indent=4)

    def merge_json_files(self):
        all_files = []
        for json_file in self.json_dir.glob('*.json'):
            with json_file.open('r') as f1:
                data = json.load(f1)
            all_files.append(data)

        with (self.path_name / f'{self.json_file_name}.json').open('w') as f2:
            json.dump(all_files, f2, indent=4)
        print(f'Merged all JSON files as {self.json_file_name}.json')
        shutil.rmtree(self.json_dir)
        self.completed()
        return all_files

    def completed(self):
        full_path = self.path_name / f'{self.json_file_name}.json'
        print(f'JSON files merged successfully!\n{self.json_file_name}.json saved at: {full_path}')

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
                print(value)
            if exception_type == FileNotFoundError:
                self.json_exporter.create_directory()
            else:
                (self.json_exporter.path_name / f'{self.json_exporter.json_file_name}.json').unlink()
            self.restart_program(f'{self.json_exporter.json_file_name}')
    
    def restart_program(self, file):
        print(Path.cwd())
        file_name = f'{file}.json'
        (Path.cwd() / 'FileCraftsman' / file_name).unlink()
        main()

async def main():
    logging.basicConfig(level=logging.INFO)
    web_scraper = AsyncWebScraper(limit=2)
    parsed_data = await web_scraper.parse_urls()
    if parsed_data:
        json_exporter = JSONExporter()
        unique_filename = json_exporter.generate_unique_filename()
        with ThreadPoolExecutor() as executor:
            list(executor.map(json_exporter.export_data, parsed_data))
        try:
            json_exporter.merge_json_files()
        except (FileNotFoundError, shutil.Error) as e:
            LogPathHandler(json_exporter).handle_error(type(e))

if __name__ == "__main__":
    asyncio.run(main())