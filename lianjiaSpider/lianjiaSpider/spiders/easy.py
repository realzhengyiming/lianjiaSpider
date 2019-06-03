# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from scrapy.loader import ItemLoader
from ..items import shortInfoHome

class EasySpider(CrawlSpider):
    name = 'easy'
    allowed_domains = ['lianjia.com']
    # start_urls = ['https://sz.lianjia.com/zufang/']
    start_urls = []

    # 广州市内含有的 https://www.lianjia.com/city/ 参考这儿。
    # locationCode = ['dg', 'fs', 'gz', 'hui', 'jiangmen', 'qy', 'sz',
                    # 'zh', 'zhanjiang', 'zs']


    locationCode = ['bj']  # 目前只放了广东/省，都是以拼音开头，只留一个广州的用来测试。
    headUrl = 'https://{}.lianjia.com/zufang/pg{}/#contentList'  # 前面{}是地方，后面{}是页数，最多100页
    count = 0
    zufangCount = 0


    def close(self,spider, reason):
        print(self.count)
        print("zufang")
        print(self.zufangCount)
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
            for page in range(1,101 ):  # 1~100 （1，101）
                self.start_urls.append(self.headUrl.format(location,page))
            for url in self.start_urls:
                # print(url)
                yield scrapy.Request(url, dont_filter=False)
                print()
                # 这里重写爬虫入口方法，将dont_filter设置为false

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//p[@class='content__list--item--title twoline']"), callback='parse_item', follow=True),
    )


    # 看url可以看出两种url 一种是公寓，一种是租房的。
    ## 公寓有公寓设施
    ## 租房有租房信息数据


    def parse_item(self, response): # 上面是提取链接，下面是打开链接

        # print(response.text )
        # print(response.url)
        # 暂时先不处理公寓的，所以剩下的都是租房的

        if response.url.find("/apartment/")!= -1 :
            # https://gz.lianjia.com/apartment/10066.html 这个是公寓，公寓是没有发布时间的。
            # print(response.text)
            self.count += 1
            headContent = response.xpath("//meta[@name='keywords']/@content").extract()
            # print(headContent)
            postTime = response.xpath('//*[@id="map"]/div[1]/div[3]/div/img[11]/@src').extract()
            # print("发布时间")
            # print(postTime)
            i = {}
            # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
            # i['name'] = response.xpath('//div[@id="name"]').extract()
            # i['description'] = response.xpath('//div[@id="description"]').extract()
            # return i


        # todo         if response.url.find("/apartment/")!= -1 :
        else:   # 那就只取这种租用的。
            print(response.url)
            self.zufangCount+=1
            # 这个是租房的东西  https://gz.lianjia.com/zufang/GZ2202604301950656512.html
            headContent = response.xpath("//meta[@name='keywords']/@content").extract()
            area = response.xpath('//*[@id="aside"]/ul[1]/p/span[3]/text()').extract()
            areaNum = area[0].split("㎡")[0]
            price = response.xpath('//*[@id="aside"]/p[1]/span/text()').extract()[0]
            title,location = headContent[0].split(",")[0],headContent[0].split(",")[2]
            # print(title)
            tempTitle = title.split(" ")
            homeName, roomContent, direction = "","",""
            if len(tempTitle)==4:
                homeName, roomContent, direction = tempTitle[0], tempTitle[1]+"-"+tempTitle[2], tempTitle[3],

            if len(tempTitle)==3:
                homeName,roomContent,direction = tempTitle

            if location.find("房屋出租")!=-1:
                location = location.replace("房屋出租","")

            postTime = response.xpath("//div[@class='content__subtitle']/text()").extract()
            print("发布时间")
            # 提取时间
            pattern = re.compile(r'(\d{4}-\d{1,2}-\d{1,2})')  # 查找里面的日期字符串，发布日期，好像只有租房的才有，公寓没有。
            postTimeResult = pattern.findall("".join(postTime))[0]



            newsloader = ItemLoader(item=shortInfoHome(), response=response)  # 但是使用这种方法插入进去的都会是list。
            newsloader.add_value('homeName', homeName)
            newsloader.add_value('location', location)
            newsloader.add_value('area', areaNum)
            newsloader.add_value('direction', direction)
            newsloader.add_value('price', price)
            newsloader.add_value('roomContent', roomContent)

            newsloader.add_value('homeUrl', response.url)
            newsloader.add_value("postDate", postTimeResult)

            yield newsloader.load_item()
            print( newsloader.load_item()
)

            pass

        print()