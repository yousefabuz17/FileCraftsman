import json
import asyncio
import os
from pathlib import Path
from async_web_scraper import *
from concurrent.futures import ThreadPoolExecutor

class Craftsman:
    def __init__(self):
        console.print('[bold green]\n\tCRAFTSMAN ACTIVATED[/bold green]')
        self.current_dir = Path.cwd() / 'FileCraftsman' if Path.cwd().name=='Projects' else Path.cwd()
        self.data = self.get_data()

    def create_dirs(self):
        os.makedirs(self.current_dir / 'RandomFolder', exist_ok=True)
        for i in range(3):
            os.makedirs(self.current_dir / 'RandomFolder' / f'RandomSubFolder{i}', exist_ok=True)
            for j in range(3):
                os.makedirs(self.current_dir / 'RandomFolder' / f'RandomSubFolder{i}' / f'RandomSubSubFolder{j}', exist_ok=True)

    def write_to_file(self):
        json_data = self.get_data()
        folder_path = self.current_dir / 'RandomFolder'
        for idx, json_item in enumerate(json_data):
            sub_folder_path = folder_path / f'RandomSubFolder{idx % 3}' / f'RandomSubSubFolder{idx // 3}'
            os.makedirs(sub_folder_path, exist_ok=True)
            file_path = sub_folder_path / f'random_file{idx}.txt'
            with open(file_path, 'w') as file:
                file.write(
                        f"{json_item['tag_names']}\n",
                        f"{json_item['tag_text']}\n",
                        f"{json_item['tag_text']}\n",
                        f"{json_item['random_bytes']}\n",
                        f"{json_item['tag_contents']}\n")

    def get_data(self):
        json_file = self.current_dir / 'full_data.json'
        with open(json_file, 'r') as file:
            data = json.load(file)
        return data

    def complete(self):
        total_files = [list(map(len, [subfolder,files])) for _, subfolder, files in os.walk(self.current_dir / 'RandomFolder')]
        sub_folders_len = sum([i[0] for i in total_files])
        file_count = sum([i[-1] for i in total_files])
        console.print(
                    f"Created {file_count} files and {sub_folders_len} sub-folders",
                    '[bold red]\n\tCRAFTSMAN COMPLETE[/bold red]',
                    sep='\n')

async def main():
    data = Craftsman()
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as executor:
        await loop.run_in_executor(executor, data.create_dirs)
        await loop.run_in_executor(executor, data.write_to_file)
    data.complete()

if __name__ == '__main__':
    json_file_path = Path.cwd() / 'full_data.json'
    if not json_file_path.exists():
        asyncio.run(scraper_main())  # Run the async web scraper first to obtain the JSON file if it doesn't exist
        asyncio.run(main())
    else:
        asyncio.run(main())
