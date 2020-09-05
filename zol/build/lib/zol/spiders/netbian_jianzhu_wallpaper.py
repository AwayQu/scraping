import scrapy


class NetBianJianZhuSpider(scrapy.Spider):
    name = "netbian_jianzhu"


    def start_requests(self):
        urls = ['http://www.netbian.com/jianzhu/']
        for i in range(2, 9):
            urls.append('http://www.netbian.com/jianzhu/index_{}.htm'.format(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for detail_url in response.css("#main > div.list > ul > li > a ::attr(href)").extract():
            self.log("deatail_url %s" % detail_url)
            self.log("url join %s" % response.urljoin(detail_url))
            yield scrapy.Request(response.urljoin(detail_url), callback=self.parse_wallpaper_detail_page)

    def parse_wallpaper_detail_page(self, response):
        self.log("parse detail")

        for img_view_url in response.css("#main > div.endpage > div > div > a ::attr(href)").extract():
            self.log("image view url %s" % img_view_url)
            yield scrapy.Request(response.urljoin(img_view_url), callback=self.parse_img)

    def parse_img(self, response):
        self.log(" start parse img")
        index = 0
        for img_url in response.css("div#main > table > tr > td > a > img ::attr(src)").extract():
            index += 1
            if index == 2:
                break
            self.log("image url %s" % img_url)
            self.log("index %d" % index)
            yield {"img": img_url}

