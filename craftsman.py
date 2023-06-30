import os, requests, json
from pathlib import Path
from bs4 import BeautifulSoup

# Class for webscraping
#   This class will be used to scrape stories and random information from the web
#   to be added into text files to be manipulated and practiced with
    # 1. Method to request & parse contents from different webpages
    # 2. Method to retrieve random information from webpages
    # 3. Method to merge all contents into an organized json file
    # 4. Get method to retrieve contents from json file

# Class for Craftsman
#   This class will be used to create random directories and text files
#   to be used for practicing and learning
    # 1. Method to check current directory
        # 1a. If current directory is not Desktop, change to Desktop
        # 1b. If current directory is Desktop, make the first testing directory
    # 2. Method to create a specific set of numbered directories
    # 3. Method to create a specific set of numbered text files
        # 3a. Change to be set based on user input instead of hard coded
    # 4. Method to create the directories first, then generate the text files
        # 4a. Fetch the generated information from the webscraper class to be added onto the text files
