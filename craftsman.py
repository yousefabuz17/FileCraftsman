import json
from pathlib import Path
from async_web_scraper import *

class Craftsman:
    def __init__(self, json_file):
        self.json_file = json_file
        self.json_file_path = Path.cwd()  / 'FileCraftsman' / self.json_file
        self.json_data = json.load(open(self.json_file_path, 'r'))

    def get_data(self):
        return self.json_data

def main():
    craftsman = Craftsman('full_data.json').get_data()

if __name__ == '__main__':
    asyncio.run(scraper_main()) # Run the async web scraper first to obtain the JSON file
    main()