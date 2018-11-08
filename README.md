<p style="font-size:24px;font-weight:800">markdown语法</p>

***创建环境***
>引用
>>标题1
>>>hhh
---
[百度一下](http://www.baidu.com)
+ 列表
+ 列表2
   1. 嘿嘿   
   2. 嘻嘻
   3. 哈哈
   
课程表|星期一|星期二
:---:|:---:|:---:
第一节|语文|数学
第二节|体育|英语

```
public static void main (String[] args){
    System.out.println("hello world!")
}
```

---

<p style="font-size:24px;font-weight:800">Scrapy爬虫练习</p>

<p>开发环境的搭建</p>
**pipenv**  

pip 使用豆瓣源安装 scrapy

`pip install -i https://pypi.douban.com/simple/ scrapy `

创建Scrapy项目   
`scrapy startproject ArtcleSpider`  

创建网站爬虫模板  
`scrapy genspider jobber blog.jobble.com` 
 
生成如下代码
```python
import scrapy


class JobberSpider(scrapy.Spider):
    name = 'jobber'
    allowed_domains = ['blog.jobber.com']
    start_urls = ['http://blog.jobber.com/']

    def parse(self, response):
        pass

```
pip问题降级  
```
python -m pip install pip==18.0

#其中，-m参数的解释：
run library module as a script (terminates option list)
将库中的python模块用作脚本去运行。
```

<p>settings.py中取消robot协议防止爬虫终止  </p>

```python
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
```
###Xpath使用方法

表达式|说明
:---:|:---
nodename | 选取此节点的所有节点
/ | 从根节点选取
// | 从匹配选择的当前节点选择文档中的节点，而不考虑他们的位置
.|选取当前节点
..|选取当前节点的父节点
@|选取属性

使用scrapy  shell  url 终端分析网页
```
 title = response.xpath('//*[@id="post-107390"]/div[1]/h1/text()')
 text()取出值
```


###CSS选择器
...


##Scrapy Item

###Pipelines 代表数据流处理管道
```python
# 取消注释 数字代表管道处理的优先级  数字越小  则优先级越高
# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'ArticleSpider.pipelines.ArticlespiderPipeline': 300,
   'scrapy.pipelines.images.ImagesPipeline':50,
}
```

爬去数据录入数据库
```
pipenv install pymysql
```

配置mysql异步插入 提高解析速度   
mysql的配置信息在setting文件中
```python
#setting.py 文件中
MYSQL_HOST = ''
MYSQL_DBNAME = ''
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_PORT = 3306

from twisted.enterprise import adbapi 
import pymysql
#使用twisted实现异步录入
class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
        
    #此方法会被自动调用  将setting文件中的配置信息传入读取
    @classmethod
    def from_setting(cls,settings):
        host = settings['MYSQL_HOST']
        db = settings['MYSQL_DBNAME']
        user = settings['MYSQL_USER']
        password = settings['MYSQL_PASSWORD']
        port = settings['MYSQL_PORT']
        
        db_params = dict(
            host = host,
            db = db,
            user = user,
            password = password,
            charset = 'utf-8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True
        )
        
        dbpool = adbapi.ConnectionPool('MySQLdb',**db_params)
        return cls(dbpool)
        
    def process_item(self,item,spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        #处理异常
        query.addErrback(self.handle_error)
        
    def handle_error(self,failure):
        #处理异常
        print(failure)
        
    def do_insert(self,cursor,item):
        pass
```

###Item Loader机制 
封装匹配规则 及对提取出的字段数据做特殊处理
```python
from scrapy.loader import ItemLoader
import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst
from ArticleSpider.items import ArticleDetailItem
def parser_detail(response):
    # article_item = ArticleDetailItem()
    item_loader = ItemLoader(item = ArticleDetailItem(),response=response)
    item_loader.add_css("title",".entry-header h1::text")
    item_loader.add_value("url",response.url)
    article_item = item_loader.load_item()
    yield article_item 
    
#使用 MapCompose 可以传入多个处理函数  会依次调用
title = scrapy.Field(
    input_processor=MapCompose(lambda x : x + "prefix"),
    output_processor = TakeFirst() 
)
``` 


#知乎爬虫
####知乎的登录  
selenium 安装  pip install selenium  
安装浏览器驱动 
```python
from selenium import webdriver
from scrapy.selector import Selector

browser = webdriver.Chrome(executable_path="驱动路径")
browser.get("url")

#动态加载完成之后的网页内容
page_source = browser.page_source

selector  = Selector(text=page_source)

```

####模拟知乎登录
```python
#兼容模式导入python2或python3
try:
    import cookielib
except:
    import http.cookiejar as cookiejar
    
import requests
    

def get_xsrf():
    response = requests.get("https://www.zhihu.com",headers=header)
```

requests和requests.session()区别  session 复用链接不需要再次建立连接了

新建知乎爬虫项目 scrapy genspider zhihu www.zhihu.com   

```bash
scrapy shell -s USER-AGENT="" url 
#设置user-agent
```

####数据表设计

爬取代码
```python
try:
    import urlparse as parse
except:
    from urllib import parse 
    
from scrapy import Request

import scrapy
import re

class ZhihuSpider(scrapy.Spider):
    
    def parse(self,response):
        post_urls = response.css("a:attr(href)").extract()
        post_urls = [parse.urljoin(response.url,url) for url in post_urls if url.startWith("https://")]
        # post_urls = filter(lambda x : True if x.startswith("https://") else False,post_urls)
        
        for url in post_urls:
            match_obj =  re.match(r"(.*zhihu.com/question/(\d+))($|/).*",url)
            if match_obj:
                question_url = match_obj.group(1)
                question_id = match_obj.group(2)
                
            yield Request(url=url,callback=self.parse_question)
    def parse_question(self,response):
        pass
```
安装本地软件包 "pip install file_path" 


#招聘网站整站爬取

以上爬虫使用的都是默认basic模板
```bash
#列出所有可用scrapy模板
scrapy genspider --list
Available templates:
  basic
  crawl
  csvfeed
  xmlfeed

#指定scrapy模板生成爬虫项目
scrapy genspider -t crawl lagou www.lagou.com
```

####Crawl爬取流程分析
+ 继承自CrawlSpider，默认复写了parse方法，因此我们不能再将parse作为默认的解析函数了
```python

import copy
import six

from scrapy.http import Request, HtmlResponse
from scrapy.utils.spider import iterate_spider_output
from scrapy.spiders import Spider

class CrawlSpider(Spider):
    rules = ()

    def __init__(self, *a, **kw):
        super(CrawlSpider, self).__init__(*a, **kw)
        #初始编译rule规则
        self._compile_rules()
    
    
    def _compile_rules(self):
        def get_method(method):
            if callable(method):
                return method
            elif isinstance(method, six.string_types):
                return getattr(self, method, None)
        #循环遍历rule规则
        self._rules = [copy.copy(r) for r in self.rules]
        for rule in self._rules:
            #解析回到函数
            rule.callback = get_method(rule.callback)
            rule.process_links = get_method(rule.process_links)
            rule.process_request = get_method(rule.process_request)
    
    #被覆写了默认处理解析函数
    def parse(self, response):
        return self._parse_response(response, self.parse_start_url, cb_kwargs={}, follow=True)


    #解析入口
    def _parse_response(self, response, callback, cb_kwargs, follow=True):
        #从start_url开始爬取时没有回调函数是parse_start_url [] 跳过 
        if callback:
            cb_res = callback(response, **cb_kwargs) or ()
            cb_res = self.process_results(response, cb_res)
            for requests_or_item in iterate_spider_output(cb_res):
                yield requests_or_item
        
        if follow and self._follow_links:
            for request_or_item in self._requests_to_follow(response):
                yield request_or_item
                
    #抽取页面中符合规则的url 比对所有url规则
    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        #这里很nice 将rule的序号取出来 通过_build_request传递出去
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                #符合规则的url创建Request
                r = self._build_request(n, link)
                yield rule.process_request(r)
                
    #符合规则的url创建Request
    def _build_request(self, rule, link):
        #设置回调  rule为序号
        r = Request(url=link.url, callback=self._response_downloaded)
        r.meta.update(rule=rule, link_text=link.text)
        return r

    def _response_downloaded(self, response):
        #通过rule在rules中的序号 定位到response对应的callback等信息
        rule = self._rules[response.meta['rule']]
        #再次进入循环  callback 没有设置的仅作为匹配页面不做提取操作
        return self._parse_response(response, rule.callback, rule.cb_kwargs, rule.follow)


                
    def parse_start_url(self, response):
        return []

    def process_results(self, response, results):
        return results



    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CrawlSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider._follow_links = crawler.settings.getbool(
            'CRAWLSPIDER_FOLLOW_LINKS', True)
        return spider

    def set_crawler(self, crawler):
        super(CrawlSpider, self).set_crawler(crawler)
        self._follow_links = crawler.settings.getbool('CRAWLSPIDER_FOLLOW_LINKS', True)
```


