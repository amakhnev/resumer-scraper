import scrapy


class OutsideIr35Spider(scrapy.Spider):
    name = "outside_ir35"
    allowed_domains = ["outsideir35.org.uk"]
    start_urls = ["https://outsideir35.org.uk/"]

    def parse(self, response: scrapy.http.Response):
        self.logger.info("Scaffold spider reached %s", response.url)
        return []
