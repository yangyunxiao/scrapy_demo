# _*_ encoding:utf-8 _*_
__author__ = 'xiao'
__date__ = '2018/10/29 15:25'

import re

try:
    import cookielib
except:
    import http.cookiejar as cookielib
import requests

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookie.txt")

try:
    session.cookies.load(ignore_discard=True)
except:
    print("加载cookie失败")
header = {
    "user-agent": USER_AGENT,
    "Referer": "https://www.zhihu.com",
    "HOST": "www.zhihu.com"
}


def login():
    login_url = "https://www.zhihu.com/signup?next=/"
    response = requests.get(login_url, headers=header)

    pass

def get_captcha():
    import time
    t = str(int(time.time()) * 1000)
    captcha_url = ""

    captcha_file_name = "captcha.jpg"

    t = session.get(captcha_url,headers = header)
    with open(captcha_file_name,"wb") as f:
        f.write(t.content)
        f.close()

    from PIL import Image
    try:
        im = Image.open("captcha_file_name")
        im.show()
        im.close()
    except:
        pass

    captcha = int("输入验证码\n")
    return captcha

def zhihu_login(account, password):
    phone_num_pattern = r"^1\d{10}$"
    if re.match(phone_num_pattern, account):
        print("手机号码登录")
        post_params = {

        }
        login_url = ""
    else:
        if "@" in account:
            print("邮箱登录")
            post_params = {

            }
            login_url = ""

    login_response = session.post(url=login_url, data=post_params, headers=header)
    session.cookies.save()


if __name__ == "__main__":
    # login()

    account = "13931288111"
    pattern = r"^1\d{10}$"
    if re.match(pattern, account):
        print("匹配成功")
    else:
        print("匹配失败")
