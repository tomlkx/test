import json
import time
import random

import scrapy
import codecs

'''
 公司高管页面爬取
'''


class T2Spider(scrapy.Spider):
    name = "t2"
    allowed_domains = ["vip.stock.finance.sina.com.cn"]
    start_urls = []
    with open('stock-list.txt', 'r', encoding='utf-8') as f:
        for i in f.readlines():
            start_urls.append(
                'https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpManager/stockid/' + i.split(".")[
                    0] + '.phtml')
    f.close()
    print(start_urls[0])

    def parse(self, response):
        time.sleep(random.randint(1, 3))
        items = []
        gpCode = '股票代码'
        gpCodeValue = response.xpath('/html/body/div[6]/div[2]/div[1]/div[1]/div[1]/a[4]/h1/span/text()').get()
        for i in response.xpath('//*[@id="comInfo1"]'):
            lb = i.xpath('thead/tr/th/text()').get()
            jb = ''
            print(lb)
            for trs in i.xpath('tbody/tr')[1:]:
                # 调试使用
                # print(len(trs.xpath('td').getall()))
                name, zw, start_time, stop_time = '', '', '', ''
                if len(trs.xpath('td').getall()) > 1:
                    # 姓名
                    name = trs.xpath('td[1]/div/a/text()').get()
                    # 职务
                    zw = trs.xpath('td[2]/div/text()').get()
                    # 起始日期
                    start_time = trs.xpath('td[3]/div/text()').get()
                    # 终止日期
                    stop_time = trs.xpath('td[4]/div/text()').get()
                else:
                    jb = trs.xpath('td/div/text()').get().replace('\r\n\t\t', '').strip()
                items.append(
                    {'姓名': name, '职务': zw, '起始日期': start_time, '终止日期': stop_time, '届别': jb, '部门': lb,'股票代码': gpCodeValue})
        with open('公司高管_data_json.txt', 'a', encoding='utf-8') as f:
            for i in items:
                f.write('||'.join(i.values()) + '\n')
        f.close()
        pass
