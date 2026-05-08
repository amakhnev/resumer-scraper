import scrapy


class JobItem(scrapy.Item):
    external_url_normalized = scrapy.Field()
    external_url_raw = scrapy.Field()
    title = scrapy.Field()
    employer_name = scrapy.Field()
    recruiter_name = scrapy.Field()
    country_code = scrapy.Field()
    city = scrapy.Field()
    location_text = scrapy.Field()
    work_mode = scrapy.Field()
    ir35_status = scrapy.Field()
    rate_min = scrapy.Field()
    rate_max = scrapy.Field()
    rate_unit = scrapy.Field()
    currency = scrapy.Field()
    posted_at = scrapy.Field()
    description_raw = scrapy.Field()
    description_clean = scrapy.Field()
    source_quality = scrapy.Field()
    parser_confidence = scrapy.Field()
    content_hash = scrapy.Field()
