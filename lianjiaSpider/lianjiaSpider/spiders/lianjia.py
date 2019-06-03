# -*- coding: utf-8 -*-
import scrapy


class LianjiaSpider(scrapy.Spider):
    # todo 这边暂时只处理普通租房，不处理公寓的信息。
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    # start_urls = ['https://sz.lianjia.com/zufang/']
    start_urls = []

    # 广州市内含有的 https://www.lianjia.com/city/ 参考这儿。
    # locationCode = ['dg', 'fs', 'gz', 'hui', 'jiangmen', 'qy', 'sz',
                    # 'zh', 'zhangjiang', 'zs']

    locationCode = ['gz']  # 目前只放了广东省，都是以拼音开头，只留一个广州的用来测试。
    headUrl = 'https://{}.lianjia.com/zufang/pg{}/#contentList'  # 前面{}是地方，后面{}是页数，最多100页

    def close(spider, reason):
        print("链家爬虫跑完了。")
        # 这儿重写一下，我只写页面的具体内容的解析就可以了。

    def start_requests(self):
        '''
        北上广深的几个地方都可以都放到这里面来的。
        广东省的这几个城市
        东莞 dg ,佛山 fs ,广州 gz ,惠州 hz,江门 jm, 清远 qy ,深圳 sz,
        珠海 zh,湛江 zj,中山 zs
        :return:
        '''
        for location in self.locationCode:
            for page in range(1, 101):  # 1~100
                self.start_urls.append(self.headUrl.format(location,page))
            for url in self.start_urls:
                print(url)
                yield scrapy.Request(url, dont_filter=False)
                print()
                # 这里重写爬虫入口方法，将dont_filter设置为false

    def parse(self, response):
        '''
        提取每个列表页的 房子详情页 的url，再传给 detailParse
        :param response:
        :return:
        '''



        pass

    def detailParse(self, response):
        pass
