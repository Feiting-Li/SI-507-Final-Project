
# NBA Topshot Data Scraper

This Python script scrapes data from the NBA Topshot marketplace and extracts information about various collectibles. The data includes links, rarity, player names, lowest asking prices, average sales, and more.

Users can choose which players' or teams' data they want to know and export a csv file of the data

## Requirements

- Python 3.6+
- BeautifulSoup4
- Selenium
- WebDriver (e.g., geckodriver for Firefox)
- questionary

Ensure you have the above Python libraries installed. You can install them using pip:

```bash
pip install beautifulsoup4 selenium questionary
```

You also need to have the appropriate WebDriver installed for Selenium. This script uses Firefox, so you would need `geckodriver`, which you can download from [Mozilla's GitHub](https://github.com/mozilla/geckodriver/releases).

## Installation

Clone the repository or download the `.py` file to your local machine.

## Usage

Run the script from the command line:

```bash
python DataStructure.py
```

The script will prompt you to select the number of pages you wish to scrape. It will then automatically scrape the data, which can take several minutes depending on the number of pages.

After scraping, the script will print out the list of collected players. You can then input the name of the player or team you're interested in, and the script will output their data and save it to a CSV file in the current working directory.

## Output

The script saves the scraped data to a CSV file named `topshot_data_<currentdate>.csv`.

## Notes

- Make sure to have a stable internet connection while running the script.
- The script might need adjustments if the website structure changes.
