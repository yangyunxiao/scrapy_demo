# _*_ encoding:utf-8 _*_
__author__ = 'xiao'
__date__ = '2018/10/22 15:07'

import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    md = hashlib.md5()
    md.update(url)
    return md.hexdigest()
