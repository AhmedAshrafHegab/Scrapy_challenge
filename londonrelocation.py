import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from property import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        all_div_area = response.css('div.test-inline')
        for info in all_div_area:

            title = info.css(".h4-space a::text").get().strip()
            location_url_temp = info.css(".h4-space a::attr(href)").get()
            location_url_temp2 = "https://londonrelocation.com/"
            location_url = location_url_temp2+location_url_temp
            price_array = info.css("h5::text").get().strip().split(" ")
            price = int(price_array[1])
            if "pw" in price_array[2]:
                price = price*4

            yield {
                'location_url': location_url,
                'title': title,
                'price': price
            }
            # property = ItemLoader(item=Property())
            # property.add_value('title', title)
            # property.add_value('price', price)  # 420 per week
            # property.add_value('url', location_url)
            # return property.load_item()

        next_page = response.css(".pagination a::attr(href)").get().replace('1', '2')
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_area_pages)
