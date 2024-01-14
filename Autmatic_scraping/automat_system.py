# # automat_system.py
# import multiprocessing
# from apscheduler.schedulers.background import BackgroundScheduler
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from competitors.comp_scraper.comp_scraper.spiders.cop_spider import CompetitorsSpider
# from fred_scraping.fred_scraping.spiders.astro_spider import AstroSpider
# from yahoo_finance.yahoo_finance.spiders.yahoo_finance import YahooFinanceSpider
# import time
#
#
# def run_spider(spider_cls):
#     process = CrawlerProcess(get_project_settings())
#     process.crawl(spider_cls)
#     process.start()
#
#
# def run_spiders():
#     spider_classes = [CompetitorsSpider] #, AstroSpider, YahooFinanceSpider]
#     with multiprocessing.Pool(processes=len(spider_classes)) as pool:
#         pool.map(run_spider, spider_classes)
#
#
# def schedule_spiders():
#     scheduler.add_job(run_spiders, trigger='cron', hour=15, minute=22)
#     scheduler.start()
#
#
# def main():
#     print("Scheduling spiders to run every morning at 12:05 AM...")
#     schedule_spiders()
#
#     try:
#         while True:
#             time.sleep(1)
#     except (KeyboardInterrupt, SystemExit):
#         scheduler.shutdown()
#
#
# if __name__ == '__main__':
#     scheduler = BackgroundScheduler()
#     main()

# Import necessary modules and classes
import multiprocessing
from apscheduler.schedulers.background import BackgroundScheduler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from competitors.comp_scraper.comp_scraper.spiders.cop_spider import CompetitorsSpider
from fred_scraping.fred_scraping.spiders.astro_spider import AstroSpider
from yahoo_finance.yahoo_finance.spiders.yahoo_finance import YahooFinanceSpider
from datetime import datetime, timedelta
import time

MINUTES = 60


# Function to run a specific spider class
def run_spider(spider_cls):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_cls)
    process.start()


# Function to run multiple spiders using multiprocessing
def run_spiders():
    # List of spider classes to be executed
    spider_classes = [CompetitorsSpider]  # , AstroSpider, YahooFinanceSpider]

    # Create a multiprocessing pool to run spiders concurrently
    with multiprocessing.Pool(processes=len(spider_classes)) as pool:
        pool.map(run_spider, spider_classes)


# Function to schedule spider execution using apscheduler
def schedule_spiders():
    # Calculate the time difference for the countdown timer
    now = datetime.now()
    scheduled_time = datetime(now.year, now.month, now.day, 18, 30)
    time_difference = scheduled_time - now

    # Print the initial countdown timer
    print(
        f"Scraping will start in {int(time_difference.total_seconds() // 60)} minutes and {int(time_difference.total_seconds() % 60)} seconds.")

    # Define a function to update and print the countdown dynamically
    def update_countdown():
        nonlocal time_difference
        time_difference -= timedelta(seconds=1)
        print(
            f"Scraping will start in {int(time_difference.total_seconds() // 60)} minutes and {int(time_difference.total_seconds() % 60)} seconds.")

    next_spider_run = MINUTES * 24
    # Add a job to run_spiders with a countdown timer
    scheduler.add_job(run_spiders, trigger='interval', hours=24, start_date=scheduled_time)  # Change minutes=1 to
    # scheduler.add_job(run_spiders, trigger='interval', minutes=1, start_date=scheduled_time)
    # days=1
    # Add a separate job to update and print the countdown every second
    scheduler.add_job(update_countdown, trigger='interval', seconds=1, start_date=now, end_date=scheduled_time)
    scheduler.start()


# Main function
def main():
    # Print a message indicating the scheduling of spiders
    print("Scheduling spiders to run every morning at 12:05 AM...")

    # Schedule spiders
    schedule_spiders()

    try:
        # Keep the main process running
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        # Shutdown the scheduler on keyboard interrupt or system exit
        scheduler.shutdown()


# Entry point of the script
if __name__ == '__main__':
    # Initialize the BackgroundScheduler
    scheduler = BackgroundScheduler()

    # Call the main function
    main()
