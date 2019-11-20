import scrapy
import re
from wanfang.items import WanfangItem
from scrapy.selector import Selector
from scrapy import Request


# from scrapy import log

class WanfangSpider(scrapy.Spider):
    name = 'wanfang'
    allowed_domains = ["wanfangdata.com.cn"]
    start_urls = [
        'http://c.old.wanfangdata.com.cn/PeriodicalSubject.aspx?NodeId=T.TP&IsCore=true'
    ]
    # http://s.wanfangdata.com.cn/Paper.aspx?q=%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B+DBID%3aWF_QK&f=top&p=578
    cookies = {}

    headers = {
        # 'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    meta = {
        'dont_redirect': True,
        'handle_httpstatus_list': [301, 302]
    }

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse, headers=self.headers, cookies=self.cookies,
                      meta=self.meta)

    def __init__(self):
        self.count = 0
        self.url_1 = 'http://c.old.wanfangdata.com.cn/PeriodicalSubject.aspx?NodeId=T.TP&IsCore=true'

    def parse(self, response):
        # 这里已经获得了核心期刊列表页的内容，接下来工作是抽取期刊的英文缩写
        sel = Selector(response)
        periodical_strs = []
        for i in range(1, 49):
            # 加@href链提取链接
            # 从中提取出的链接是：Periodical-bgzdh.aspx，下面是提取bgzdh的示例
            # str = 'Periodical-bgzdh.aspx'
            # result1 = re.sub(r'.*-', '', str)
            # result2 = result1.split('.')
            # print(result2[0])
            periodical_url = sel.xpath(
                '/html/body/div[@class="content content-c"]/div[@class="nav-panel clear"]/div[@class="nav-right"]/div[@class="list"]/span[@class="link-wraper col-3"][' + str(i) + ']/a[@class="link"]/@href').extract()[0]
            rm_left = re.sub(r'.*-', '', periodical_url)
            periodical_str = rm_left.split('.')[0]
            periodical_strs.append(periodical_str)
        # 接下来按 年 月 期刊名 进行逐一爬取（这个顺序是为了保证对所有期刊雨露均沾）
        # 样例链接 http://c.old.wanfangdata.com.cn/periodical/bgzdh/2019-9.aspx
        base_str = 'http://c.old.wanfangdata.com.cn/periodical/'
        for month in reversed(range(1, 10)):
            for p_str in periodical_strs:
                url = base_str + p_str + '/2019-' + str(month) + '.aspx'
                yield Request(url, callback=self.get_page)

        for year in reversed(range(2010, 2019)):
            for month in reversed(range(1, 13)):
                for p_str in periodical_strs:
                    url = base_str + p_str + '/' + str(year) + '-' + str(month) + '.aspx'
                    yield Request(url, callback=self.get_page)

    # 获取该页所有论文链接
    def get_page(self, response):
        sel = Selector(response)
        urls = sel.xpath(
            '/html/body/div[@id="wrap3"]/div[@class="maincontent"]/div[@class="Content_div_detail"]/ul[@class="qkcontent_ul"]/li/a[@class="qkcontent_name"]/@href').extract()
        for url in urls:
            yield Request(url, callback=self.get_one)

    # 获取单篇论文信息
    # c_title = scrapy.Field()  # 中文标题
    # e_title = scrapy.Field()  # 英文标题
    #
    # url = scrapy.Field()  # 链接
    #
    # c_author = scrapy.Field()  # 作者姓名 中文
    # e_author = scrapy.Field()  # 作者姓名 英文
    #
    # c_periodical = scrapy.Field()  # 期刊名称 中文
    # e_periodical = scrapy.Field()  # 期刊名称 英文
    #
    # indexID = scrapy.Field()  # 年，卷（期）
    #
    # c_abstract = scrapy.Field()  # 摘要 中文
    # e_abstract = scrapy.Field()  # 摘要 英文
    #
    # c_keywords = scrapy.Field()  # 关键字 中文
    # e_keywords = scrapy.Field()  # 关键字 英文
    #
    # time = scrapy.Field()  # 出版日期
    # fund = scrapy.Field()  # 基金项目
    def get_one(self, response):
        sel = Selector(response)
        item = WanfangItem()
        c_title = sel.xpath('/html/body/div[@class="fixed-width baseinfo clear"]/div[@class="section-baseinfo"]/h1/text()').extract()
        e_title = sel.xpath('/html/body/div[@class="fixed-width baseinfo clear"]/div[@class="section-baseinfo"]/h2/text()').extract()
        url = response.url
        c_author = sel.xpath('/html/body/div[@class="fixed-width-wrap fixed-width-wrap-feild"]/div[@class="fixed-width baseinfo-feild"]/div[@class="row row-author"][1]/span[@class="text"]/a/text()').extract()
        e_author = sel.xpath('/html/body/div[@class="fixed-width-wrap fixed-width-wrap-feild"]/div[@class="fixed-width baseinfo-feild"]/div[@class="row row-author"][2]/span[@class="text"]/a/text()').extract()
        c_periodical = sel.xpath('/html/body/div[@class="fixed-width-wrap fixed-width-wrap-feild"]/div[@class="fixed-width baseinfo-feild"]/div[@class="row row-magazineName"][1]/span[@class="text"]/a/text()').extract()
        e_periodical = sel.xpath('/html/body/div[@class="fixed-width-wrap fixed-width-wrap-feild"]/div[@class="fixed-width baseinfo-feild"]/div[@class="row row-magazineName"][2]/span[@class="text"]/a/text()').extract()
        indexID = sel.xpath('/html/body/div[@class="fixed-width-wrap fixed-width-wrap-feild"]/div[@class="fixed-width baseinfo-feild"]/div[@class="row"][3]/span[@class="text"]//text()').extract()
        c_abstract = sel.xpath('/html/body/div[@class="fixed-width baseinfo clear"]/div[@class="section-baseinfo"]/div[@class="baseinfo-feild abstract"]/div[@class="row clear zh"]/div[@class="text"]/text()').extract()
        c_keywords = sel.xpath('/html/body/div[@class="fixed-width-wrap fixed-width-wrap-feild"]/div[@class="fixed-width baseinfo-feild"]/div[@class="row row-keyword"]/span[@class="text"]/a/text()').extract()
        time = sel.xpath('/html/body/div[@class="fixed-width-wrap fixed-width-wrap-feild"]/div[@class="fixed-width baseinfo-feild"]/div[@class="row"][5]/span[@class="text"]/text()').extract()
        fund = sel.xpath('/html/body/div[@class="fixed-width-wrap fixed-width-wrap-feild"]/div[@class="fixed-width baseinfo-feild"]/div[@class="row"][6]/span[@class="text"]/text()').extract()
        units = sel.xpath('/html/body/div[@class="fixed-width-wrap fixed-width-wrap-feild"]/div[@class="fixed-width baseinfo-feild"]/div[@class="row"][2]/span[@class="text"]//text()').extract()
        item['c_title']=c_title
        item['e_title']=e_title
        item['url']=url
        item['c_author']=c_author
        item['e_author']=e_author
        item['c_periodical']=c_periodical
        item['e_periodical']=e_periodical
        item['indexID']=indexID
        item['c_abstract']=c_abstract
        item['c_keywords']=c_keywords
        item['time']=time
        item['fund']=fund
        item['units'] =units
        yield item
