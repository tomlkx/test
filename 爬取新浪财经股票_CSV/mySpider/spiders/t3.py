import json

import scrapy
import time
import random


class T3T4T5Spider(scrapy.Spider):
    name = "t3_t4_t5"
    allowed_domains = ["vip.stock.finance.sina.com.cn"]
    start_urls = []
    with open('stock-list.txt', 'r', encoding='utf-8') as f:
        for i in f.readlines():
            start_urls.append(
                'https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpXiangGuan/stockid/' + i.split(".")[
                    0] + '.phtml')
    f.close()
    print(start_urls[0])

    def parse(self, response):
        time.sleep(random.uniform(1, 3))
        # 相关证券
        xg_items = []
        # 所属指数
        sszs_items = []
        # 所属系
        ss_items = []
        gpCode = '股票代码'
        gpCodeValue = response.xpath('/html/body/div[6]/div[2]/div[1]/div[1]/div[1]/a[4]/h1/span/text()').get()
        for i in response.xpath('//*[@class="comInfo1"]'):
            lb = i.xpath('thead/tr/th/text()').get()
            jb = ''
            print(lb)
            for trs in i.xpath('tbody/tr')[1:]:
                # 调试使用
                # print(len(trs.xpath('td').getall()))
                t1 = trs.xpath('td[1]/div')
                t2 = trs.xpath('td[2]/div')
                # 进入日期
                start_time = trs.xpath('td[3]/div/text()').get()
                # 退出日期
                stop_time = trs.xpath('td[4]/div/text()').get()
                if lb == '相关证券':
                    xg_items.append({
                        '品种代码': t1.xpath('a/text()').get() if t1.xpath('a/text()').get() is not None else t1.xpath(
                            'text()').get(),
                        '品种简称': t2.xpath('a/text()').get() if t2.xpath('a/text()').get() is not None else t2.xpath(
                            'text()').get(),
                        '股票代码': gpCodeValue
                    })
                elif lb == '所属指数':
                    sszs_items.append({
                        '指数名称': t1.xpath('text()').get(),
                        '指数代码': t2.xpath('text()').get(),
                        '进入日期': trs.xpath('td[3]/div/text()').get() if trs.xpath(
                            'td[3]/div/text()').get().replace('\xa0', '') is not None else '',
                        '退出日期': trs.xpath('td[4]/div/text()').get().replace('\xa0', '') if trs.xpath(
                            'td[4]/div/text()').get() is not None else '',
                        '股票代码': gpCodeValue
                    })
                else:
                    ss_items.append({
                        '公司系': t1.xpath('text()').get(),
                        '股票代码': gpCodeValue
                    })

        # print(xg_items)
        with open('相关证券_data_json.txt', 'a', encoding='utf-8') as f1:
            for i in xg_items:
                f1.write('||'.join(i.values()) + '\n')
        f1.close()
        # print(sszs_items)
        with open('所属指数_data_json.txt', 'a', encoding='utf-8') as f2:
            for i in sszs_items:
                f2.write('||'.join(i.values()) + '\n')
        f2.close()

        # print(ss_items)
        with open('所属系_data_json.txt', 'a', encoding='utf-8') as f3:
            for i in ss_items:
                f3.write('||'.join(i.values()) + '\n')
        f3.close()
        pass
