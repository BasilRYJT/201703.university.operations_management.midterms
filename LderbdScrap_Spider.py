import scrapy
import time

class OMSpider(scrapy.Spider):
    name = "TestScrap"
    start_urls = ["http://op.responsive.net/lt/sharma/entry.html"]

    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'id': 'group404', 'password': 'group404'},
            callback=self.after_login
        )

    def after_login(self, response):
        if "Invalid team id or password!" in response.body:
            self.logger.error("Login failed")
            return

        else:
            url = "http://op.responsive.net/Littlefield/Standing"
            yield scrapy.Request(
                url,
                callback=self.parse_lderbd
            )
    def parse_lderbd(self,response):
        if response.body:
            lderbd = {}
            if response.css("td+ td font::text").extract():
                lderbd["time"] = time.time()
                for i in range(len(response.css("td+ td font::text").extract())/2):
                    lderbd[response.css("td+ td font::text").extract()[2*i]] = response.css("td+ td font::text").extract()[2*i+1]
            yield lderbd
            yield scrapy.Request(
                response.url,
                callback=self.parse_lderbd,
                dont_filter=True
            )
        else:
            url = "http://op.responsive.net/lt/sharma/entry.html"
            yield scrapy.FormRequest.from_response(
                url,
                formdata={'id': 'group404', 'password': 'group404'},
                callback=self.after_login
            )