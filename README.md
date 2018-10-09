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





