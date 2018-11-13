# _*_ encoding:utf-8 _*_
import requests
from scrapy import Selector

__author__ = 'xiao'
__date__ = '2018/11/13 15:12'


def crawl_ips():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }
    page_text = requests.get("http://www.xicidaili.com/nn/",headers = headers)

    selector = Selector(text=page_text)
    ip_tr_selectors = selector.css("#ip_list tr")
    for ip_tr_selector in ip_tr_selectors:
        print()
    pass


if __name__ == "__main__":
    crawl_ips()
