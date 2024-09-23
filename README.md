# Termux Onion Crawler

## Overview
The **Termux Onion Crawler** is a Python script designed to scrape `.onion` links from specified Tor hidden service directories. The crawler can operate in both single-pass and recursive modes, allowing users to explore hidden services effectively while managing the output of the discovered links.

## Features
- **URL Input:** Users can input any `.onion` directory URL to scrape, with a default option provided.
- **Link Extraction:** The script extracts clickable and non-clickable `.onion` links using BeautifulSoup and regex.
- **Recursive Crawling:** Optionally visit random `.onion` links found during scraping for deeper exploration.
- **Logging:** Activity is logged to both the console and a file for tracking the crawling process.
- **Link Saving:** Extracted links can be saved to a specified file for later use.
- **Customizable Sleep Interval:** Users can set a sleep interval between requests to manage traffic.

## Installation
1. Ensure you have Python installed on your Termux environment.
2. Install required packages:
   ```bash
   pkg install python
   pip install requests beautifulsoup4 lxml
   ```
3. Clone the repository or download the `crawl.py` file to your Termux directory.

## Usage
Run the script with the following command:

```bash
python crawl.py
```

Follow the on-screen prompts to enter the desired `.onion` directory URL, choose whether to save the links to a file, and decide if you want to enable recursive crawling.

### Parameters
- **URL:** The `.onion` directory you wish to scrape (default: `https://thehiddenwiki.org/`).
- **Save to file:** Choose whether to save extracted links to a file.
- **Recursive crawling:** Decide if you want to crawl randomly linked `.onion` pages.

## Logging
Logs will be created to track the status of the crawl, including:
- Successful page accesses
- Extracted links
- Errors encountered during the process

Logs are output both to the console and to a file named `extracted_onion_links.txt` if the saving option is enabled.

## Notes
- Ensure your Termux environment is configured to access the Tor network before running the crawler.
- The use of this script must comply with legal regulations and ethical considerations regarding internet scraping and privacy.

## Disclaimer
This script is intended for educational purposes only. Use responsibly and within the bounds of the law.

---

**Created by Isaac**
