import scrapy


class ZolJianZhuSpider(scrapy.Spider):
    name = "zol_jianzhu"


    def start_requests(self):
        urls = [
            'http://desk.zol.com.cn/jianzhu/',
            'http://desk.zol.com.cn/jianzhu/2.html',
            'http://desk.zol.com.cn/jianzhu/3.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for detail_url in response.css("ul.pic-list2 > li.photo-list-padding > a.pic ::attr(href)").extract():
            self.log("deatail_url %s" % detail_url)
            self.log("url join %s" % response.urljoin(detail_url))
            yield scrapy.Request(response.urljoin(detail_url), callback=self.parse_wallpaper_detail_page)

    def parse_wallpaper_detail_page(self, response):
        self.log("parse detail")
        for img_view_url in response.css("ul#showImg > li > a ::attr(href)").extract():
            self.log("image view url %s" % img_view_url)
            yield scrapy.Request(response.urljoin(img_view_url), callback=self.parse_img)

    def parse_img(self, response):
        index = 0
        for img_url in response.css("dd#tagfbl > a ::attr(href)").extract():
            index += 1
            if index == 2:
                break
            self.log("image url %s" % img_url)
            self.log("index %d" % index)
            yield scrapy.Request(response.urljoin(img_url), callback=self.get_img)


    def get_img(self, response):

        index = 0
        for img_url in response.css("body > img ::attr(src)").extract():
            index += 1
            if index == 2:
                break
            self.log("real image url %s" % img_url)
            yield {"img": img_url}

