# -*- coding: utf-8 -*-
import scrapy


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        pass

    def start_requests(self):
        from selenium import webdriver
        # browser = webdriver.Chrome(executable_path='/Users/xiao/Desktop/Google Chrome.app/Contents/MacOS/chromedriver')
        browser = webdriver.Chrome(executable_path="/Applications/Google Chrome.app/Contents/MacOS/chromedriver")
        browser.get("https://www.zhihu.com/signup")

        browser.find_element_by_css_selector(".SignContainer-switch span").click()
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("97598032@qq.com")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys("anying1114")

        browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()

        import time
        time.sleep(10)

        Cookies = browser.get_cookies()

        print(Cookies)


        pass