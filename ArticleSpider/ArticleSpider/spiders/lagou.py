# -*- coding: utf-8 -*-
import io

import pickle
import scrapy
import sys

import time

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    #Q:为什么这里的callback不用函数self.parse_item传递
    #A: because this is a class instance ，can not use self. key
    rules = (
        Rule(LinkExtractor(allow=r'jobs/.*'), follow=True),
        Rule(LinkExtractor(allow=r'/zhaopin/.*'), callback='parse_job', follow=True),
    )

    def parse_job(self,response):
        print("hahha" + response.url)

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

    def start_requests(self):
        from selenium import webdriver
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
        chrome_opt = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_opt.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(executable_path="/Users/xiao/Applications/Google Chrome.app/Contents/MacOS/chromedriver", chrome_options=chrome_opt)
        browser.get("https://passport.lagou.com/login/login.html?service=https%3a%2f%2fwww.lagou.com%2f")
        browser.find_elements_by_css_selector(".input.input_white")[0].send_keys("97598032@qq.com")
        browser.find_elements_by_css_selector(".input.input_white")[1].send_keys("anying1114")
        # browser.find_element_by_xpath("/html/body/section/div[1]/div[2]/form/div[2]/input").send_keys(password)
        browser.find_element_by_css_selector(".btn.btn_green.btn_active.btn_block.btn_lg").click()
        time.sleep(10)
        Cookies = browser.get_cookies()
        cookie_dict = {}
        for cookie in Cookies:
            f = open('./ArticleSpider/cookies/lagou/' + cookie['name'] + '.lagou', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

