from async_web_scraper import *
from pathlib import Path
import json

class Craftsman:
    def __init__(self):
        self.json_file_path = Path.cwd()  / 'FileCraftsman' / 'full_data.json'
        self.json_data = json.load(open(self.json_file_path, 'r'))

    def get_data(self):
        return self.json_data


def main():
    craftsman = Craftsman().get_data()

if __name__ == '__main__':
    asyncio.run(scraper_main()) # Run the async web scraper first to obtain the JSON file
    main()