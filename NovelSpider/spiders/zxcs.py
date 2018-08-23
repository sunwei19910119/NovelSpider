# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from scrapy.http import Request
from urllib import parse
from NovelSpider.items import ZxcsItem
from scrapy.loader import ItemLoader

class ZxcsSpider(scrapy.Spider):
    name = 'zxcs'
    allowed_domains = ['www.zxcs8.com']
    # start_urls是一个待爬的列表，
    #spider会为我们把请求下载网页做到，直接到parse阶段
    start_urls = ['http://www.zxcs8.com/sort/55']



    def parse(self, response):
        # 提取出html页面中的所有url，并跟踪这些url进一步爬取。
        # 如果提取的url中格式为/post/xxx 就下载之后直接进入解析函数
        all_urls = response.xpath('//dl[@id="plist"]/dt[1]/a/@href').extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]

        for url in all_urls:
            match_obj = re.match("(.*zxcs8.com/post/(\d+))(/|$).*", url)
            if match_obj:
                # 如果提取到小说相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, callback=self.parse_novel)
            else:
                # 注释这里方便调试
                pass
        # 提取下一页并交给scrapy进行下载
        next_url = response.xpath('//div[@id="pagenavi"]/span/following-sibling::a[1]/@href').extract_first("")

        if next_url:
            # 如果还有next url 就调用下载下一页，回调parse函数找出下一页的url。
            yield Request(url=next_url, callback=self.parse)




    def parse_novel(self,response):
        # 在小说详情页面进一步解析
        title = response.xpath('//div[@id="content"]/h1/text()').extract_first("")
        download_page = response.xpath('//div[@class="down_2"]/a/@href').extract_first("")
        #请求下载页
        yield scrapy.Request(download_page, callback=self.download)

    def download(self,response):
        # 实例化
        item_loader = ItemLoader(item=ZxcsItem(), response=response)
        item_loader.add_xpath('file_urls','//div[@class="content"]/div[@class="panel"][1]//span[@class="downfile"][1]/a/@href')
        # item_loader.add_xpath('file_urls','//span[@class="downfile"][1]/a/@href')
        zxcs_item = item_loader.load_item()

        # 已经填充好了值调用yield传输至pipeline
        yield zxcs_item



