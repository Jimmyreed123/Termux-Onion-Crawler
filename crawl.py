import requests
import re
from bs4 import BeautifulSoup
import time
import logging
import random
import os

# Setup logging to output to file and console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def crawl_onion_directory(url, recursive=False, sleep_interval=60, save_to_file=False, save_path=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    visited_urls = set()  # Track visited URLs to avoid revisiting

    def scrape_page(url):
        try:
            # Sending the GET request with headers
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                logging.info(f"Successfully accessed {url}.")
                
                # Parse the response text with BeautifulSoup
                soup = BeautifulSoup(response.text, "lxml")

                # Extract clickable .onion links from anchor tags
                clickable_onion_links = [
                    link.get('href') for link in soup.find_all('a') 
                    if link.get('href') and '.onion' in link.get('href')
                ]

                # Extract non-clickable .onion links using regex for v2 and v3 onion addresses
                non_clickable_onion_links = re.findall(r'[a-z2-7]{16}\.onion|[a-z2-7]{56}\.onion', soup.text)

                # Combine both lists of links, avoiding duplicates
                all_onion_links = list(set(clickable_onion_links + non_clickable_onion_links))

                # Filter out any previously visited links
                new_links = [link for link in all_onion_links if link not in visited_urls]

                # Print or log extracted .onion links
                if new_links:
                    logging.info(f"Extracted {len(new_links)} new .onion links from {url}.")
                    for link in new_links:
                        logging.info(link)

                    # Optionally save to a file
                    if save_to_file and save_path:
                        file_path = os.path.join(save_path, "extracted_onion_links.txt")
                        with open(file_path, "a") as file:
                            for link in new_links:
                                file.write(link + '\n')
                        logging.info(f"Links saved to {file_path}")
                else:
                    logging.info(f"No new .onion links found on {url}.")
                
                return new_links
            else:
                logging.warning(f"Failed to access {url}. Status code: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP request error: {e}")
            return []
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return []

    # Recursive crawling function
    def recursive_crawl(starting_url):
        current_url = starting_url

        while True:
            visited_urls.add(current_url)
            logging.info(f"Currently crawling: {current_url}")
            links_on_page = scrape_page(current_url)

            if not links_on_page:
                logging.info(f"No new links found on {current_url}. Stopping recursive crawl.")
                break

            # Select a random link from the newly found links
            next_url = random.choice(links_on_page)
            logging.info(f"Selecting random link to visit: {next_url}")
            current_url = next_url

            # Sleep before continuing to the next page
            time.sleep(sleep_interval)

    # If not recursive, scrape the initial page and stop
    if not recursive:
        scrape_page(url)
    else:
        recursive_crawl(url)

# Main function to prompt the user for the directory URL and scraping options
def main():
    print("Welcome to the Onion Link Scraper!")
    
    # Ask the user for a URL to scrape
    url = input("Please enter the URL of the directory you want to scrape (press Enter for default 'https://thehiddenwiki.org/'): ")
    
    # Use default URL if the user leaves it blank
    if not url:
        url = "https://thehiddenwiki.org/"
        print(f"No URL entered, defaulting to {url}.")

    # Ask the user if they want to save results to a file
    save_option = input("Do you want to save the extracted links to a file? (y/n): ").lower()
    save_to_file = save_option == 'y'

    # Ask the user if they want to enable recursive crawling
    recursive_option = input("Do you want to enable recursive crawling (visiting random links)? (y/n): ").lower()
    recursive = recursive_option == 'y'

    # If saving to file, ask for a save path
    save_path = None
    if save_to_file:
        save_path = input("Please enter the directory where you want to save the file (leave blank for current directory): ")
        
        # Default to current directory if the user doesn't provide a path
        if not save_path:
            save_path = os.getcwd()
            print(f"Defaulting to current directory: {save_path}")

        # Create the directory if it doesn't exist
        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path)
                print(f"Created directory: {save_path}")
            except Exception as e:
                print(f"Error creating directory: {e}")
                return

    # Infinite loop to crawl periodically with configurable interval
    while True:
        crawl_onion_directory(url, recursive=recursive, sleep_interval=60, save_to_file=save_to_file, save_path=save_path)
        if not recursive:
            logging.info("Sleeping for 60 seconds before the next round of crawling...")
            time.sleep(60)

# Entry point for the program
if __name__ == "__main__":
    main()