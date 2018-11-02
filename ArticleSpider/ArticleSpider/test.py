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

    for x in test_yield(0, 100, 5):
        if isinstance(x , str):

            print("last yield {0}" .format(x))

        else :
            print("first yield {0}".format(x))
