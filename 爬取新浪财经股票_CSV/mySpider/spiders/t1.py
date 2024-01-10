import random
import time
import json
import scrapy
from scrapy.selector import Selector


class ItcastSpider(scrapy.Spider):
    # 这个爬虫的识别名称，必须是唯一的，在不同的爬虫必须定义不同的名字。
    name = "t1"
    # 是搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页，不存在的URL会被忽略。
    allowed_domains = ["vip.stock.finance.sina.com.cn"]
    # 爬取的URL元祖/列表。爬虫从这里开始抓取数据，所以，第一次下载的数据将会从这些urls开始。其他子URL将会从这些起始URL中继承性生成。
    start_urls = []
    with open('stock-list.txt', 'r', encoding='utf-8') as f:
        for i in f.readlines():
            start_urls.append(
                'https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/' + i.split(".")[0] + '.phtml')
    f.close()
    print(start_urls[0])
    '''
    描述:
        解析的方法，每个初始URL完成下载后将被调用，调用的时候传入从每一个URL传回的Response对象来作为唯一参数，主要作用如下
            1.负责解析返回网页数据response.body,提取结构化数据生成(item)
            2.生成需要下一页的URL
    总结:
        通俗易懂的来说,也就是所谓的处理逻辑,你需要完成的提取操作全在这里完成就行了
    '''
    def parse(self, response):
        time.sleep(random.randint(1, 3))
        list_1 = []
        list_2 = []
        print(f"--------------{response.xpath('/html/body/div[6]/div[2]/div[1]/div[1]/div[1]/a[4]/h1/span/text()').extract()[0]}--------------")
        list_1.append('股票代码')
        list_2.append(response.xpath('/html/body/div[6]/div[2]/div[1]/div[1]/div[1]/a[4]/h1/span/text()').extract()[0])
        for i in response.xpath('//*[@id="comInfo1"]/tr'):
            number = 0
            for item in i.xpath('td'):
                number += 1
                if number % 2 != 0:
                    list_1.append(item.xpath('text()').extract()[0])
                else:
                    if len(item.xpath('text()').extract()) == 0 or len(item.xpath('text()').extract()) > 1 or item.xpath('text()').extract()[0].strip() == '':
                        list_2.append(
                            item.xpath('a/text()').extract()[0] if len(item.xpath('a/text()').extract()) > 0 else '')
                    else:
                        list_2.append(item.xpath('text()').extract()[0])
        zd = (dict(zip(list_1, list_2)))
        zd['公司简介：'] = response.xpath('/html/body/div[6]/div[2]/div[3]/table[1]/tr[20]/td[2]/text()').extract()[0]
        with open('公司简介_data_json.txt', 'a', encoding='utf-8') as f:
            f.write('||'.join(zd.values())+'\n')
        f.close()
