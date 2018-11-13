# _*_ encoding:utf-8 _*_
__author__ = 'xiao'
__date__ = '2018/10/30 13:48'


def test_yield(start, end, step=1):
    if start >= end:
        return

    while start < end:
        start += step
        import time
        time.sleep(2)
        yield start

    yield  "heiheihahei"


if __name__ == "__main__":

    # for x in test_yield(0, 100, 5):
    #     if isinstance(x , str):
    #
    #         print("last yield {0}" .format(x))
    #
    #     else :
    #         print("first yield {0}".format(x))

    from fake_useragent import UserAgent
    ua = UserAgent()
    print(ua.random)

    print(getattr(ua,"random"))
    dict = dict(age=1)
    dict.age = 11
    dict.setdefault("name","yunxioa")
    dict.__setitem__('name', "hahhh")
    print(getattr(dict,"age"))
