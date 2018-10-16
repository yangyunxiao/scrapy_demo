# _*_ encoding:utf-8 _*_
__author__ = 'xiao'
__date__ = '2018/10/16 10:32'

from scrapy.cmdline import execute
import sys, os

sys.path.append(os.path.abspath(__file__))

execute(["scrapy", "crawl", "jobbole"])
