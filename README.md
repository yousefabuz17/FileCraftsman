# File Craftsman
The File Craftsman is a Python project that showcases advanced web scraping techniques and file manipulation capabilities. It allows users to generate random text files, create directories, and scrape web pages to extract valuable information. The project demonstrates the use of asynchronous programming, JSON data handling, and efficient file management.

## Features
- **Random File Generation:** The program generates a specified number of random text files with customizable content. Users can define the number of files, file names, and content length to simulate real-world scenarios for testing or experimentation.

- **Directory Creation:** The project includes a directory creation feature that generates directories with random names and a specified number of subdirectories. This functionality helps users simulate complex folder structures and practice file operations.

- **Advanced Web Scraping:** The web scraping feature utilizes the aiohttp library for asynchronous HTTP requests and the BeautifulSoup library for HTML parsing. Users can specify the number of URLs to scrape and retrieve valuable information from reliable sources. The scraped data is organized and stored in JSON format for further analysis.

- **JSON Exporter:** The project includes a JSONExporter class that handles the export of scraped data. It generates unique filenames for each JSON file and merges them into a single file for easy access and analysis. The JSONExporter class demonstrates efficient file management techniques and ensures the integrity of the exported data.

## Installation
Make sure you have Python installed (version 3.6 or later).
Clone or download the repository to your local machine.

git clone https://github.com/yousefabuz17/FileCraftsman.git

## Usage
Open a terminal or command prompt and navigate to the project directory.
Run the following command to start the program:
```shell
python craftsman.py
python3 craftsman.py
```

# Contributing
Contributions to File Craftsman project are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request on the project's GitHub repository.

## Acknowledgements
The File Craftsman project utilizes various open-source libraries and resources. Special thanks to the developers and contributors of the following libraries:
- aiohttp: Asynchronous HTTP client/server framework
- BeautifulSoup: HTML parsing library
- uuid: Universally unique identifier generation
- pathlib: Object-oriented filesystem paths
- concurrent.futures: Asynchronous execution of callables
