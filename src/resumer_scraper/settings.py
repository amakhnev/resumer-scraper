BOT_NAME = "resumer_scraper"

SPIDER_MODULES = ["resumer_scraper.spiders"]
NEWSPIDER_MODULE = "resumer_scraper.spiders"

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS_PER_DOMAIN = 2
AUTOTHROTTLE_ENABLED = True
