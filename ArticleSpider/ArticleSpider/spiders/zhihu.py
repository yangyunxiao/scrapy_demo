# -*- coding: utf-8 -*-
import urllib
from urllib import parse
import re
import scrapy
from scrapy import Request

from ArticleSpider.items import ZhiHuQuestionItem, ArticleItemLoader


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        all_urls = response.css("a::attr(href)").extract()

        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https://") else  False, all_urls)
        # 'https://www.zhihu.com/question/264186020/answer/524739650'
        for url in all_urls:
            question_pattern = r"^(.*.zhihu.com/question/(\d+))(/|$).*"
            question_matcher = re.match(question_pattern, url)
            if question_matcher:
                question_url = question_matcher.group(1)
                question_id = question_matcher.group(2)
                yield Request(url=question_url, headers=self.headers,
                              meta={"question_id": question_id}, callback=self.parse_question)
            else:
                # 如果不是问题页面 则继续深入爬取
                yield Request(url=url, headers=self.headers)

    def parse_question(self, response):
        zhihu_question_item = ArticleItemLoader(item=ZhiHuQuestionItem(), response=response)

        zhihu_question_item.add_css('title', "h1.QuestionHeader-title::text")
        zhihu_question_item.add_value("question_id", response.meta.get('question_id', 0))
        zhihu_question_item.add_css("question_detail", ".QuestionHeader-detail")
        zhihu_question_item.add_css("tags", ".Tag-content .Popover div::text")
        # zhihu_question_item.add_css("follow_nums", ".QuestionFollowStatus .NumberBoard-itemValue")
        zhihu_question_item = zhihu_question_item.load_item()

        yield zhihu_question_item

    def start_requests(self):
        from selenium import webdriver
        # browser = webdriver.Chrome(executable_path='/Users/xiao/Desktop/Google Chrome.app/Contents/MacOS/chromedriver')
        browser = webdriver.Chrome(
            executable_path="/Users/xiao/Applications/Google Chrome.app/Contents/MacOS/chromedriver")
        browser.get("https://www.zhihu.com/signup")

        browser.find_element_by_css_selector(".SignContainer-switch span").click()
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("97598032@qq.com")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys("anying1114")

        browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()

        import time
        time.sleep(5)

        cookies = browser.get_cookies()

        print(cookies)

        cookie_dict = {}
        import pickle
        for cookie in cookies:
            f = open("./ArticleSpider/cookies/zhihu/" + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return [Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict, headers=self.headers)]
