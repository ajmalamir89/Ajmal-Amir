
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from competitors.comp_scraper.comp_scraper.spiders.cop_spider import CompetitorsSpider

from fred_scraping.fred_scraping.spiders.astro_spider import AstroSpider
from yahoo_finance.yahoo_finance.spiders.yahoo_finance import YahooFinanceSpider
import time


def run_spider(spider_class):
    # Create a Scrapy CrawlerProcess with project settings
    process = CrawlerProcess(get_project_settings())

    # Run the specified spider class
    process.crawl(spider_class)

    # Start the process
    process.start()


def main():
    print("Choose a spider to run:")
    print("1. CompetitorsSpider")
    print("2. AstroSpider")
    print("3. YahooFinanceSpider")

    choice = input("Enter the number corresponding to the spider you want to run: ")

    if choice == '1':
        run_spider(CompetitorsSpider)
    elif choice == '2':
        run_spider(AstroSpider)
    elif choice == '3':
        run_spider(YahooFinanceSpider)
    else:
        print("Invalid choice. Please enter a valid number.")
        return

    # Add a delay before exiting to allow the spider to complete
    time.sleep(10)


if __name__ == '__main__':
    main()
