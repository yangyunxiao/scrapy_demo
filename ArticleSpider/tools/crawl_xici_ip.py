# _*_ encoding:utf-8 _*_
import requests
from scrapy import Selector
from datetime import datetime

__author__ = 'xiao'
__date__ = '2018/11/13 15:12'
import pymysql

mysql_config = dict(
    host="127.0.0.1",
    user="root",
    password="",
    db="article_spider",
    port=3306,
    charset="utf8",
    use_unicode=True
)

conn = pymysql.connect(**mysql_config)
cursor = conn.cursor()


def crawl_ips():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    }

    for x in range(2):
        proxy_url = "http://{0}:{1}".format("203.93.125.238", 31566)
        proxy_config = {
            "http": proxy_url
        }
        url = "http://www.xicidaili.com/nn/{0}".format(x)
        print("url {0}".format(url))

        page_text = requests.get(url=url, headers=headers, proxies=proxy_config)

        print("code {0}  text {1}".format(page_text.status_code ,page_text.text))
        selector = Selector(text=page_text.text)

        ip_tr_selectors = selector.css("#ip_list tr")
        ip_list = []
        for ip_tr_selector in ip_tr_selectors[1:]:
            td_texts = ip_tr_selector.css("td::text").extract()
            td_texts = list(map(lambda text: text.strip(), td_texts))
            ip = td_texts[0]
            port = td_texts[1]
            type = td_texts[5]
            ip_list.append((ip, type, port))

        for ip_entry in ip_list:
            print("ip : {0}  port : {1}  type : {2}".format(ip_entry[0], ip_entry[1], ip_entry[2]))
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = """
                INSERT INTO `xici_ips` (`ip`,`type`,`port`,`update_time`)
                VALUES ('{0}','{1}','{2}','{3}')
                ON DUPLICATE KEY UPDATE `update_time`=VALUES(update_time)
            """
            cursor.execute(sql.format(ip_entry[0], ip_entry[1], ip_entry[2], current_time))
            conn.commit()


if __name__ == "__main__":
    crawl_ips()

    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.37 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    # }
    #
    # proxy_url = "http://{0}:{1}".format("121.31.137.42", 8123)
    #
    # try:
    #     proxies = {
    #         'http': proxy_url
    #     }
    #     repsonse =  requests.get(url="http://www.xicidaili.com/nn", headers=headers, proxies=proxies)
    #     text = repsonse.text
    #     pass
    # except Exception as e:
    #     print("invalid ip and port")
    #
    # import requests
    #
    # '''代理IP地址（高匿）'''
    # proxy = {
    #     'http': 'http://119.179.142.220:8060/',
    # }
    # print("dsadasdas")
    # '''head 信息'''
    # head = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',}
    # '''http://icanhazip.com会返回当前的IP地址'''
    # p = requests.get('http://text.gopaopao.com', headers=head, proxies=proxy)
    # print(p.text)
