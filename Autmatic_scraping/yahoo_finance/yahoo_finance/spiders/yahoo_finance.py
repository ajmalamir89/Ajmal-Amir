import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from yahoo_finance.yahoo_finance.spiders.ListOfCompanies import start_companies


class YahooFinanceSpider(scrapy.Spider):
    name = 'yahoo_finance'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'FEEDS': {
            'Yahoo_finance_data.json': {
                'format': 'json',
                'overwrite': True,  # Set this to True to overwrite the file each time
            },
        },
    }

    start_urls = ['https://finance.yahoo.com/quote/{}/history?p={}']

    def start_requests(self):
        for company in start_companies:
            # Construct the URL for each company
            url = self.start_urls[0].format(company, company)

            # Yield the request with the company information
            yield scrapy.Request(url, callback=self.parse, meta={'company': company})

    def parse(self, response):
        company = response.meta['company']
        self.log(f'Starting {company}')

        # options = Options()
        # options.headless = True
        # driver = webdriver.Chrome(options=options)
        # driver.get(response.url)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')  # Needed for Windows
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(response.url)

        # Wait for the historical data table to be present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody tr'))
        )

        # Scroll to the bottom of the page
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.END)

        # Scroll to the bottom of the page by sending "END" key multiple times
        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(10):  # Adjust the number of iterations as needed
            body.send_keys(Keys.END)
            time.sleep(5)  # Add a small delay between each scroll

        # Add a delay to allow the page to load
        time.sleep(15)

        # Get the updated page content
        new_response = scrapy.Selector(text=driver.page_source)

        rows = new_response.css('tbody tr')
        for row in rows:
            date = row.css('td:nth-child(1) span::text').get()
            close_price = row.css('td:nth-child(6) span::text').get()

            if date and close_price:
                yield {
                    'company': company,
                    'date': date,
                    'close_price': close_price,
                }

        driver.quit()

