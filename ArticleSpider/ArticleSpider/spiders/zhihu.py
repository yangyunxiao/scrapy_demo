# -*- coding: utf-8 -*-
import json
import urllib
from urllib import parse
import re
from urllib.parse import quote

import scrapy
import time
from scrapy import Request

from ArticleSpider.items import ZhiHuQuestionItem, ArticleItemLoader


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/', 'https://www.zhihu.com/search?type=content&q={0}']

    key_word = "锤子科技"

    query_next_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers" \
                            "?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2" \
                            "Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2" \
                            "Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2" \
                            "Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={1}&offset={2}&sort_by=default"

    # 搜索话题url
    zhihu_search_url = "https://www.zhihu.com/api/v4/search_v3?t=general&q={0}&correction=1&offset={1}&limit={2}"
    headers = {
        "HOST": "www.zhihu.com",
        "referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        """
        爬取锤子科技相关话题
        :param response:
        :return:
        """
        zhihu_search_url = self.zhihu_search_url.format(urllib.parse.quote(self.key_word), 0, 10)
        yield Request(url=zhihu_search_url, callback=self.parse_search_question, headers=self.headers)

    def parse_search_question(self, response):
        json_result = json.loads(response.text)
        is_end = json_result['paging']['is_end']
        next_url = json_result['paging']['next']

        for search_question in json_result['data']:
            if search_question['type'] == "search_result":
                if search_question['object']['type'] == "answer":
                    time.sleep(1)
                    print("question_title : {0}".format(search_question['object']['question']['name']))
                    print("content: {0}".format(search_question['object']['content']))

        if not is_end:
            next_url_pattern = r".*&limit=(\d+).*&offset=(\d+).*"
            url_matcher = re.match(next_url_pattern, next_url)
            if url_matcher:
                offset = url_matcher.group(2)
                limit = url_matcher.group(1)
                next_url = self.zhihu_search_url.format(self.key_word,offset,limit)
                yield Request(url=next_url, headers=self.headers, callback=self.parse_search_question)

    # def parse(self, response):
    #     all_urls = response.css("a::attr(href)").extract()
    #
    #     all_urls = [parse.urljoin(response.url, url) for url in all_urls]
    #     all_urls = filter(lambda x: True if x.startswith("https://") else  False, all_urls)
    #     # 'https://www.zhihu.com/question/264186020/answer/524739650'
    #     for url in all_urls:
    #         question_pattern = r"^(.*.zhihu.com/question/(\d+))(/|$).*"
    #         question_matcher = re.match(question_pattern, url)
    #         if question_matcher:
    #             question_url = question_matcher.group(1)
    #             question_id = question_matcher.group(2)
    #             yield Request(url=question_url, headers=self.headers,
    #                           meta={"question_id": question_id}, callback=self.parse_question)
    #         else:
    #             # 如果不是问题页面 则继续深入爬取
    #             yield Request(url=url, headers=self.headers)

    def parse_question(self, response):
        zhihu_question_item = ArticleItemLoader(item=ZhiHuQuestionItem(), response=response)
        question_id = response.meta.get('question_id', 0)
        zhihu_question_item.add_css('title', "h1.QuestionHeader-title::text")
        zhihu_question_item.add_value("question_id", question_id)
        zhihu_question_item.add_css("question_detail", ".QuestionHeader-detail")
        zhihu_question_item.add_css("tags", ".Tag-content .Popover div::text")
        # zhihu_question_item.add_css("follow_nums", ".QuestionFollowStatus .NumberBoard-itemValue")
        zhihu_question_item = zhihu_question_item.load_item()
        yield zhihu_question_item
        yield Request(self.query_next_answer_url.format(question_id, 20, 0), headers=self.headers,
                      callback=self.parse_answers)

    def parse_answers(self, response):
        '''
        解析回答
        '''
        answers_text = response.text
        answers_data = json.loads(answers_text)
        answers = answers_data['data']

        for answer in answers:
            print(answer)

        is_end = answers_data['paging']['is_end']
        if not is_end:
            yield Request(url=answers_data['paging']['next'], headers=self.headers, callback=self.parse_answers)

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
        start_url = self.start_urls[1].format(urllib.parse.quote(self.key_word))
        self.headers['referer'] = start_url
        return [Request(url=start_url, dont_filter=True,
                        cookies=cookie_dict, headers=self.headers)]
