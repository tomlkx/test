import json

import scrapy
import time
import random


class T4Spider(scrapy.Spider):
    name = "t4"
    allowed_domains = ["vip.stock.finance.sina.com.cn"]
    start_urls = []
    with open('stock-list.txt', 'r', encoding='utf-8') as f:
        for i in f.readlines():
            start_urls.append(f'https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpOtherInfo/stockid/{i.split(".")[0]}/menu_num/2.html')
    f.close()
    print(start_urls[0])

    def parse(self, response):
        time.sleep(random.uniform(2, 5))
        # 所属行业板块
        sshybk_items = []
        # 所属概念板块
        ssgnbk_items = []
        gpCode = '股票代码'
        gpCodeValue = response.xpath('/html/body/div[6]/div[2]/div[1]/div[1]/div[1]/a[4]/h1/span/text()').get()
        for i in response.xpath('//*[@class="comInfo1"]'):
            for trs in i.xpath('tr')[2:]:
                # 调试使用
                # print(len(trs.xpath('td').getall()))
                t1 = trs.xpath('td[1]')
                # 调试使用
                # print(i.xpath('tr[1]/td/text()').get())
                # 所属行业板块
                if i.xpath('tr[1]/td/text()').get() == '所属行业板块':
                    sshybk_items.append({
                        '所属行业板块': t1.xpath('text()').get(),
                        '股票代码': gpCodeValue
                    })
                # 所属概念板块
                else:
                    ssgnbk_items.append({
                        '概念板块': t1.xpath('text()').get(),
                        '股票代码': gpCodeValue
                    })

        with open('所属概念板块_data_json.txt', 'a', encoding='utf-8') as f1:
            for i in ssgnbk_items:
                f1.write('||'.join(i.values()) + '\n')
        f1.close()
        with open('所属行业板块_data_json.txt', 'a', encoding='utf-8') as f2:
            for i in sshybk_items:
                f2.write('||'.join(i.values()) + '\n')
        f2.close()
        pass
