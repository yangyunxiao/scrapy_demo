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

Pipelines 代表数据流处理管道
```python
# 取消注释 数字代表管道处理的优先级  数字越小  则优先级越高
# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'ArticleSpider.pipelines.ArticlespiderPipeline': 300,
   'scrapy.pipelines.images.ImagesPipeline':50,
}
```




