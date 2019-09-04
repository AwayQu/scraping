import scrapy

class ZolMeinvSpider(scrapy.Spider):
    name = "changtuimeinv"

    def start_requests(self):
        urls = [
            'http://desk.zol.com.cn/meinv/changtuimeinv/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for detail_url in response.css("ul.pic-list2 > li.photo-list-padding > a.pic ::attr(href)").extract():
            self.log("deatail_url %s" % detail_url)
            # yield scrapy.Request(response.urljoin(book_url), callback=self.parse_wallpaper_detail_page)
