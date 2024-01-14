
import scrapy
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fred_scraping.fred_scraping.spiders.urls import fred_urls


class AstroSpider(scrapy.Spider):
    name = 'Astro_Spider'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'FEEDS': {
            'Fred_data.json': {
                'format': 'json',
                'overwrite': True,  # Set this to True to overwrite the file each time
            },
        },
    }
    allowed_domains = ['fred.stlouisfed.org', 'finance.yahoo.com']
    scraped_data = []

    def start_requests(self):
        for url in fred_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        if 'fred.stlouisfed.org' in response.url:
            # Process data from fred.stlouisfed.org

            # Use a headless Chrome browser
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')  # Needed for Windows
            driver = webdriver.Chrome(options=chrome_options)  # You need to have ChromeDriver installed

            try:
                driver.get(response.url)

                # Wait for the download button to be present in the DOM
                download_button = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, 'download-button'))
                )

                # Click on the download button to trigger the dropdown
                download_button.click()

                # Wait for the CSV download link to be clickable
                download_link = WebDriverWait(driver, 90).until(
                    EC.element_to_be_clickable((By.ID, 'download-data-csv'))
                )

                # Get the href attribute of the CSV download link
                csv_url = download_link.get_attribute('href')

                # Download the CSV file
                df = pd.read_csv(csv_url)

                # Convert the DataFrame to a list of dictionaries
                records = df.to_dict(orient='records')

                # Yield records directly without any additional fields
                for record in records:
                    yield record

            except (TimeoutException, NoSuchElementException) as e:
                self.logger.error(f"Error processing {response.url}: {str(e)}")

            finally:
                driver.quit()
