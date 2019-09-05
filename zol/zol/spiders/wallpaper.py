import scrapy

class ZolMeinvSpider(scrapy.Spider):
    name = "zol"

    def start_requests(self):
        urls = [
            'http://desk.zol.com.cn/meinv/changtuimeinv/',
            'http://desk.zol.com.cn/meinv/siwa/',
            'http://desk.zol.com.cn/meinv/rihan/',
            'http://desk.zol.com.cn/meinv/xiangchemeinv/',
            'http://desk.zol.com.cn/meinv/dongmanmeinv/',
            'http://desk.zol.com.cn/meinv/yangyanmeinv/',
            'http://desk.zol.com.cn/meinv/yangyanmeinv/2.html',
            'http://desk.zol.com.cn/meinv/yangyanmeinv/3.html',
            'http://desk.zol.com.cn/meinv/gudianmeinv/',
            'http://desk.zol.com.cn/meinv/qingchunmeinv/',
            'http://desk.zol.com.cn/meinv/qingchunmeinv/2.html',
            'http://desk.zol.com.cn/meinv/qingchunmeinv/3.html',
            'http://desk.zol.com.cn/meinv/qingchunmeinv/4.html',
            'http://desk.zol.com.cn/meinv/qingchunmeinv/5.html',
            'http://desk.zol.com.cn/meinv/qingchunmeinv/6.html',
            'http://desk.zol.com.cn/meinv/qingchunmeinv/7.html',
            'http://desk.zol.com.cn/meinv/qingchunmeinv/8.html',
            'http://desk.zol.com.cn/meinv/mote/',
            'http://desk.zol.com.cn/meinv/gaoqingmeinv/',
            'http://desk.zol.com.cn/meinv/gaoqingmeinv/1.html',
            'http://desk.zol.com.cn/meinv/gaoqingmeinv/2.html',
            'http://desk.zol.com.cn/meinv/gaoqingmeinv/3.html',
            'http://desk.zol.com.cn/meinv/gaoqingmeinv/4.html',
            'http://desk.zol.com.cn/meinv/gaoqingmeinv/5.html',
            'http://desk.zol.com.cn/meinv/gaoqingmeinv/6.html',
            'http://desk.zol.com.cn/meinv/gaoqingmeinv/7.html',
            'http://desk.zol.com.cn/chemo/',
            'http://desk.zol.com.cn/chemo/2.html',
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

