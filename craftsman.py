import json
import asyncio
import os
from pathlib import Path
from async_web_scraper import *
from concurrent.futures import ThreadPoolExecutor

class Craftsman:
    def __init__(self, num_dir):
        console.print('[bold green]\n\tCRAFTSMAN ACTIVATED[/bold green]')
        self.num_dir = num_dir
        self.current_dir = Path.cwd() / 'FileCraftsman' if Path.cwd().name=='Projects' else Path.cwd()
        self.data = self.get_data()
        self.all_tags = ['tag_names', 'tag_text', 'tag_attr', 'tag_contents', 'random_bytes']

    def create_dirs(self):
        os.makedirs(self.current_dir / 'RandomFolder', exist_ok=True)
        for i in range(self.num_dir+1):
            os.makedirs(self.current_dir / 'RandomFolder' / f'RandomSubFolder{i}', exist_ok=True)
            for j in range(self.num_dir+1):
                os.makedirs(self.current_dir / 'RandomFolder' / f'RandomSubFolder{i}' / f'RandomSubSubFolder{j}', exist_ok=True)

    def write_to_file(self):
        json_data = self.get_data()
        folder_path = self.current_dir / 'RandomFolder'
        for idx, json_item in enumerate(json_data):
            sub_folder_path = folder_path / f'RandomSubFolder{idx % 3}' / f'RandomSubSubFolder{idx // 3}'
            os.makedirs(sub_folder_path, exist_ok=True)
            file_path = sub_folder_path / f'random_file{idx}.txt'
            with open(file_path, 'w') as file:
                for types in self.all_tags:
                    file.write(f"{json_item[types]}\n")
    
    get_data = lambda self: json.load(open(self.current_dir / 'full_data.json', 'r'))

    def complete(self):
        total_files = [list(map(len, [subfolder,files])) for _, subfolder, files in os.walk(self.current_dir / 'RandomFolder')]
        sub_folders_len = [i[0] for i in total_files]
        file_count = [i[-1] for i in total_files]
        creation_size = list(map(sum, [sub_folders_len, file_count]))
        console.print(
                    f"Created {creation_size[0]} directories and {creation_size[-1]} files.",
                    '[bold red]\n\tCRAFTSMAN COMPLETE[/bold red]',
                    sep='\n')

async def main():
    num_dirs = int(input('Enter the number of primary directories to create: '))
    data = Craftsman(num_dirs)
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
