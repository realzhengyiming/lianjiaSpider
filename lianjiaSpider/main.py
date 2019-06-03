# _*_ coding=utf-8 _*_
from scrapy import cmdline


if __name__ == '__main__':
    cmdline.execute("scrapy crawl easy".split())
    # cmdline.execute("scrapy crawl lianjia".split())

# todo 爬取100个请求里面的粗略信息。
# todo 爬取具体页面里面的页面继续提取信息
# todo 操作输出成 csv 或者是 写入数据库

# todo 做记录，不知道可不可以按时间来看价格的变化趋势，可以定时爬取来进行查看，每月一更对吧，这个就得使用数据库了，
## 也是可以做成大项目的。主要的技术是爬虫技术。
