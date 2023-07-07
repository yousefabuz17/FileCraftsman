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
```shell
git clone https://github.com/yousefabuz17/FileCraftsman.git
```

## Usage
Open a terminal or command prompt and navigate to the project directory.
Run the following command to start the program:
```shell
python craftsman.py
python3 craftsman.py
```

## Contributing
Contributions to File Craftsman project are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request on the project's GitHub repository.

## Acknowledgements
The File Craftsman project utilizes various open-source libraries and resources. Special thanks to the developers and contributors of the following libraries:
```shell
- aiohttp: Asynchronous HTTP client/server framework 
- BeautifulSoup: HTML parsing library
- uuid: Universally unique identifier generation
- pathlib: Object-oriented filesystem paths
- concurrent.futures: Asynchronous execution of callables
```

# In-Progress
- **Async-Web-Scraper: Completed (Needs Refactoring)**
    - Finalizing Exception Handling: Ensuring proper handling of exceptions during web scraping.
    - Implementing Timeout Error Handling: Addressing the issue of program freezes or crashes when a URL is unresponsive or times out.
    - Documentation and Comments: Adding inline comments to enhance code readability and maintainability. Updating docstrings for classes, methods, and functions to provide clear explanations and usage examples. Reviewing and enhancing the overall project documentation to provide comprehensive and user-friendly instructions.

- **FileCraftsman: Completed (Needs Exceptions)**
    - Craftsman Class: Creating the Craftsman class to encapsulate file generation and manipulation functionalities.
    - Craftsman Methods: Implementing various methods within the Craftsman class to support random file generation, directory creation, and other file operations.
    - Craftsman Tests: Writing comprehensive tests to ensure the functionality and reliability of the Craftsman class.
- **Pytests for Assurance: Not Started**
    - Developing a suite of pytest cases to thoroughly test the File Craftsman project.
    - Ensuring test coverage for critical components and edge cases.
    - Running the tests to ensure the overall quality and stability of the project.
- **Documentation and Comments: Not Started**
    - Adding inline comments to enhance code readability and maintainability.
    - Updating docstrings for classes, methods, and functions to provide clear explanations and usage examples.
    - Reviewing and enhancing the overall project documentation to provide comprehensive and user-friendly instructions.
