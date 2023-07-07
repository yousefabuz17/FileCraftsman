import os
import json
import shutil
import logging
import aiohttp
import asyncio
from uuid import uuid4
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup
from rich.console import Console
from random import sample, randint
from concurrent.futures import ThreadPoolExecutor
from links import LINKS
from ansi_colors import CODE

console = Console()


class AsyncWebScraper:
    def __init__(self, urls: list=None, limit=None):
        self.urls = self._limit_urls(urls, limit)
        console.print(
                    '[bold green]\n\tWEB SCRAPING ACTIVATED[/bold green]',
                    f"Parsing {len(self.urls)} URL{'s' if len(self.urls) > 1 else ''}", sep='\n')
        self.find_json_file()

    def _limit_urls(self, urls, limit):
        if urls is not None:
            if (limit is not None) and (limit <= len(urls)):
                urls = sample(urls, k=limit)
        else:
            limit = limit or randint(1, len(LINKS) // 4)
            urls = sample(LINKS, k=limit)
        return urls


    def find_json_file(self):
        json_file_path = (Path.cwd() / 'FileCraftsman' / 'full_data.json') if Path.cwd().name=='Projects' else Path.cwd() / 'full_data.json'
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
        self.path_name = (Path.cwd() / 'FileCraftsman') if Path.cwd().name=='Projects' else Path.cwd()
        self.json_file_name = json_file_name
        self.json_dir = Path('TempJSONFiles')
        self.json_dir.mkdir(exist_ok=True)
        console.print(f"Temporary directory created [bold blue]'{self.json_dir}'[/bold blue]: to store each parsed link.")

    def generate_unique_filename(self):
        unique_file_uuid = str(uuid4())[-3:]
        file_name = f'{self.json_dir}_{unique_file_uuid}.json'
        return file_name

    def export_data(self, data):
        filename = self.generate_unique_filename()
        file_path = self.json_dir / filename
        with file_path.open('w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def merge_json_files(self):
        all_files = []
        for json_file in self.json_dir.glob('*.json'):
            with json_file.open('r') as f1:
                data = json.load(f1)
            all_files.append(data)

        with (self.path_name / f'{self.json_file_name}.json').open('w', encoding='utf-8') as f2:
            json.dump(all_files, f2, indent=4)
        console.print(
                        f"{all_files.__len__()} JSON files created",
                        f"Merging all JSON files. File will be named: [bold cyan]'{self.json_file_name}.json'[/bold cyan]"
                        , sep='\n')
        shutil.rmtree(self.json_dir)
        sleep(1)
        self.completed()
        return all_files
    
    get_line_count = lambda self, file: sum(1 for _ in open(self.path_name / f'{file}.json'))
    
    def completed(self):
        full_path = self.path_name / f'{self.json_file_name}.json'
        json_byte_size, json_gb_size = full_path.stat().st_size, full_path.stat().st_size*1e-9
        console.print(
                        f"JSON files merged successfully!",
                        f"[bold green][SUCCESS][/bold green] {self.json_file_name}.json saved at:",
                        f"[yellow]{full_path}[/yellow]",
                        f"JSON Line/Byte Size: [bold blue]({self.get_line_count(self.json_file_name):,} ~ {json_byte_size:,} bytes ~ {json_gb_size:.2}GB)[/bold blue]",
                        "[u i]Note: More links parsed = More data = Larger file size & longer parsing time[/u i]",
                        "[bold red]\tWEB SCRAPING DE-ACTIVATED[/bold red]",
                        "[red]If any problems, please submit an issue on GitHub at:[/red]\n[link]https://github.com/yousefabuz17/FileCraftsman/issues/new[/link]\n"
                        , sep='\n')


async def scraper_main():
    try:
        logging.basicConfig(level=logging.INFO)
        web_scraper = AsyncWebScraper(limit=5)
        parsed_data = await web_scraper.parse_urls()
        if parsed_data:
            json_exporter = JSONExporter()
            json_exporter.generate_unique_filename()
            with ThreadPoolExecutor() as executor:
                list(executor.map(json_exporter.export_data, parsed_data))
            json_exporter.merge_json_files()
    except json.decoder.JSONDecodeError:
        console.print(f'[red]JSONDecodeError: URLs failed. Re-run program.[/red]')
        console.print(f'[bold red]If problem continues, please submit an issue on GitHub at:[/bold red]\n[bold blue][link]https://github.com/yousefabuz17/FileCraftsman/issues/new[/bold blue][/link]')

#TODO: Add timeout exception --  in-progress (not working yet)

if __name__ == '__main__':
    try:
        asyncio.run(scraper_main())
    except KeyboardInterrupt:
        console.print(f'\n[bold red]Keyboard Interrupt: Exiting the program[/bold red]')
        logging.info(f"{CODE['Font Color']['Red']}{CODE['Text Style']['Bold']}FILE-TERMINATED{CODE['Reset']}")
        json_data_file = (Path.cwd() / 'FileCraftsman' / 'full_data.json') if Path.cwd().name=='Projects' else Path.cwd() / 'full_data.json'
        json_temp_dir = (Path.cwd() / 'FileCraftsman' / 'TempJSONFiles') if Path.cwd().name=='Projects' else Path.cwd() / 'TempJSONFiles'
        if json_data_file.exists() or json_temp_dir.exists():
            json_data_file.unlink()
            shutil.rmtree(json_temp_dir)