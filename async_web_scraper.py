import os
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
from ansi_colors import CODE


class AsyncWebScraper:
    def __init__(self, urls=None, limit=None):
        logging.info(f"{CODE['Font Color']['Green']}{CODE['Text Style']['Bold']}WEB SCRAPING ACTIVATED{CODE['Reset']}")
        self.urls = self._limit_urls(urls, limit)
        self.find_json_file()

    def _limit_urls(self, urls, limit):
        if urls is not None:
            urls = random.sample(urls, min(limit, len(urls))) if limit else urls
        else:
            urls = random.sample(LINKS, 5) if limit is None else random.sample(LINKS, limit)
        return urls

    def find_json_file(self):
        json_file_path = Path.cwd() / 'FileCraftsman' / 'full_data.json'
        if json_file_path.exists():
            logging.info(f"{CODE['Font Color']['Blue']}{CODE['Text Style']['Bold']}JSON FILE ALREADY EXISTS{CODE['Reset']}")
            logging.info(f"{CODE['Font Color']['Blue']}{CODE['Text Style']['Bold']}Contents will be altered!!!{CODE['Reset']}")
            json_file_path.unlink()
    
    def get_tag_info(self, soup):
        all_tags = soup.find_all(True)
        tag_info = {
            'tag_names': list(set(tag.name for tag in all_tags)),
            'tag_attr': list(filter(lambda tag_attr: tag_attr, [tag.attrs for tag in all_tags if tag.attrs])),
            'tag_text': list(filter(lambda tag_text: tag_text, [tag.text for tag in all_tags if tag.text])),
            'tag_contents': [
                list(filter(lambda content: content, [sub_tag.text for sub_tag in tag.contents if sub_tag.text]))
                for tag in all_tags
            ]
        }
        return tag_info

    async def parse_url(self, url, session):
        try:
            async with session.get(url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                return self.get_tag_info(soup)
        except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorSSLError) as e:
            logging.error(f"{CODE['Font Color']['Red']}{CODE['Text Style']['Bold']}{e}{CODE['Reset']}")
            print(f'Continuing with other URLs')
            logging.info(f"{CODE['Font Color']['Green']}{CODE['Text Style']['Bold']}ALL URLs SUCCESSFULLY PARSED{CODE['Reset']}")
            return None

    async def parse_urls(self):
        all_tags = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.parse_url(url, session) for url in self.urls]
            try:
                all_tags = await asyncio.gather(*tasks)
            except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorSSLError):
                pass  # Ignore the exception and continue with other URLs
        return [tag_info for tag_info in all_tags if tag_info is not None]  # Filter out the None values


class JSONExporter:
    def __init__(self, json_file_name='full_data'):
        self.path_name = Path.cwd() / 'FileCraftsman'
        self.json_file_name = json_file_name
        self.json_dir = Path('TempJSONFiles')
        self.json_dir.mkdir(exist_ok=True)
        print(f'Temporary directory created "{CODE["Font Color"]["Blue"]}{CODE["Text Style"]["Bold"]}{self.json_dir}{CODE["Reset"]}": to store parsed links as JSON files')

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
        print(f'{CODE["Font Color"]["Green"]}JSON files merged successfully!\n{self.json_file_name}.json saved at: {full_path}{CODE["Reset"]}')
        logging.info(f"{CODE['Font Color']['Red']}{CODE['Text Style']['Bold']}WEB SCRAPING DE-ACTIVATED{CODE['Reset']}")


async def scraper_main():
    logging.basicConfig(level=logging.INFO)
    web_scraper = AsyncWebScraper(limit=10)
    parsed_data = await web_scraper.parse_urls()
    if parsed_data:
        json_exporter = JSONExporter()
        json_exporter.generate_unique_filename()
        with ThreadPoolExecutor() as executor:
            list(executor.map(json_exporter.export_data, parsed_data))
        json_exporter.merge_json_files()

def remove_garbage():
    json_data_file = (Path.cwd() / 'FileCraftsman' / 'full_data.json')
    json_temp_dir = (Path.cwd() / 'TempJSONFiles')
    if json_data_file.exists() and json_temp_dir.exists():
        json_data_file.unlink()
        shutil.rmtree(json_temp_dir)

#Add timeout exception

if __name__ == '__main__':
    try:
        asyncio.run(scraper_main())
    except KeyboardInterrupt:
        print(f'\n{CODE["Font Color"]["Red"]}Keyboard Interrupt: Exiting the program{CODE["Reset"]}')
        logging.info(f"{CODE['Font Color']['Red']}{CODE['Text Style']['Bold']}FILE-TERMINATED{CODE['Reset']}")
        json_data_file = (Path.cwd() / 'FileCraftsman' / 'full_data.json')
        json_temp_dir = (Path.cwd() / 'TempJSONFiles')
        if json_data_file.exists() and json_temp_dir.exists():
            json_data_file.unlink()
            shutil.rmtree(json_temp_dir)
    except json.decoder.JSONDecodeError as e:
        print(f'{CODE["Font Color"]["Red"]}JSONDecodeError: URLs failed. Re-run program.{CODE["Reset"]}')
        print(f'{CODE["Font Color"]["Red"]}{CODE["Text Style"]["Bold"]}If problem continues, please submit an issue on GitHub at:{CODE["Reset"]}\n{CODE["Font Color"]["Blue"]}{CODE["Text Style"]["Bold"]}https://github.com/yousefabuz17/FileCraftsman/issues/new{CODE["Reset"]}')