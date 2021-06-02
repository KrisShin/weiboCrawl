from lxml import etree
import time
import requests
import json
import pymongo
import urllib3
urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}


class DBConn:
    conn = None
    servers = "mongodb://localhost:27017"

    def connect(self):
        self.conn = pymongo.MongoClient(self.servers)

    def close(self):
        return self.conn.disconnect()

    def get_conn(self):
        return self.conn


def get_weibo_session():
    s = requests.Session()
    resp = s.get(
        "https://weibo.com/login.php?category=0", headers=headers, verify=False)
    headers['refer'] = "https://weibo.com/login.php?category=0"
    return s

def request_hot_list(s, page):
    path = "https://weibo.com/a/aj/transform/loadingmoreunlogin?ajwvr=6&category=0&page={}&lefnav=0&cursor=&__rnd={}".format(
        page, int(time.time()*1000))
    resp = s.get(
        path, headers=headers, verify=False)
    if resp.status_code != 200:
        return None
    data = json.loads(resp.text)
    return data.get('data', '')

# 具体解析细节待定
def parse_hot_list(html):
    selector = etree.HTML(html)
    hot_div_list = selector.xpath('//div[@class="UG_contents"]/ul/div')
    result = []
    for div in hot_div_list:
        div_str = etree.tostring(div,encoding='utf-8')
        title = div.xpath('.//text()')
        print(div_str.decode())
        break


def crawl():
    # db = DBConn()
    # db.connect()
    # conn = db.get_conn()
    # get_category_0(conn.test.data)
    s = get_weibo_session()
    html = request_hot_list(s, 1)
    with open("test.html", "w") as fp:
        fp.write(html)
    parse_hot_list(html)


if __name__ == '__main__':
    crawl()

