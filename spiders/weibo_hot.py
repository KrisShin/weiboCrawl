from lxml import etree
import time
import requests
import json
import pymongo
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(
    executable_path="D:\workplace\chromedriver.exe", chrome_options=chrome_options)

urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}
EXCEPTION_COUNT = 0
MAX_EXCEPTION_COUNT = 100


class DBConn:
    conn = None
    servers = "mongodb://localhost:27017"

    def connect(self):
        self.conn = pymongo.MongoClient(self.servers)

    def close(self):
        return self.conn.disconnect()

    def get_conn(self):
        return self.conn


def init_driver():
    driver.get("https://weibo.com/login.php?category=0")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="UG_contents"]/ul/div//div[@class="list_des"]'))
        )
    except Exception:
        driver.quit()
        print("driver init failed")
        exit(1)


def record_exception_count():
    global EXCEPTION_COUNT
    EXCEPTION_COUNT += 1
    if EXCEPTION_COUNT > MAX_EXCEPTION_COUNT:
        print("exceed max exception count")
        driver.quit()
        exit(1)


def get_weibo_session():
    s = requests.Session()
    resp = s.get(
        "https://weibo.com/login.php?category=0", headers=headers, verify=False)
    headers['refer'] = "https://weibo.com/login.php?category=0"
    if resp.status_code != 200:
        print("get weibo session failed")
        exit(1)
    return s


def request_hot_list(s, page):
    path = "https://weibo.com/a/aj/transform/loadingmoreunlogin?ajwvr=6&category=0&page={}&lefnav=0&cursor=&__rnd={}".format(
        page, int(time.time()*1000))
    resp = s.get(
        path, headers=headers, verify=False)
    if resp.status_code != 200:
        record_exception_count()
        return None
    data = json.loads(resp.text)
    return data.get('data', '')


def parse_hot_link(html):
    if not html:
        return None
    selector = etree.HTML(html)
    hot_div_link_list = selector.xpath(
        '//div[@class="UG_contents"]/ul/div//a[@class="a_topic"]/ancestor::div[@class="list_des"]/@href')
    result = []
    for link in hot_div_link_list:
        result.append("https:{}".format(link))
    return result


def request_hot_detail(link):
    driver.get(link)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="repeat_list"]'))
        )
    except Exception:
        record_exception_count()
        return ""
    return driver.page_source


def parse_hot_detail(html, link):
    if not html:
        return None
    selector = etree.HTML(html)
    hot_detail = {
        "mid": ''.join(selector.xpath('//div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[1]/@name')),
        "link": link,
        "publishTime": ''.join(selector.xpath('//div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[1]/@title')),
        "from": ''.join(selector.xpath('//div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[2]/text()')),
        "topicList": selector.xpath('//div[@class="WB_detail"]/div[@class="WB_text W_f14"]/a[@class="a_topic"]/text()'),
        "contentList": selector.xpath('//div[@class="WB_detail"]/div[@class="WB_text W_f14"]/text()'),
        "shareCount": ''.join(selector.xpath('//div[@class="WB_handle"]/ul/li[2]//span[@class="line S_line1"]/span//em[2]/text()')),
        "commentCount": ''.join(selector.xpath('//div[@class="WB_handle"]/ul/li[3]//span[@class="line S_line1"]/span//em[2]/text()')),
        "likeCount": ''.join(selector.xpath('//div[@class="WB_handle"]/ul/li[4]//span[@class="line S_line1"]/span//em[2]/text()'))
    }
    user_info = {
        # 头像
        "headPic": ''.join(selector.xpath('//div[@class="face"]//img[@class="W_face_radius"]/@src')),
        # 昵称
        "nickname": ''.join(selector.xpath('//div[@class="WB_detail"]/div[@class="WB_info"]/a[@class="W_f14 W_fb S_txt1"]/text()')),
        # 主页
        "homepage": "https:{}".format(''.join(selector.xpath('//div[@class="WB_detail"]/div[@class="WB_info"]/a[@class="W_f14 W_fb S_txt1"]/@href'))),
    }
    hot_detail['user'] = user_info
    return hot_detail


def crawl(total, conn):
    count = 0
    page = 1

    init_driver()
    s = get_weibo_session()
    while True:
        html = request_hot_list(s, page)
        link_list = parse_hot_link(html)
        if not link_list:
            record_exception_count()
            continue
        for link in link_list:
            detail_html = request_hot_detail(link)
            hot_detail = parse_hot_detail(detail_html, link)
            mid = hot_detail.get('mid', '')
            if not hot_detail or mid == '':
                record_exception_count()
                continue
            conn.test.data.insert_one(hot_detail)
            break
        break


def main():
    db = DBConn()
    db.connect()
    conn = db.get_conn()

    try:
        crawl(10, conn)
    finally:
        conn.close()
        driver.quit()


if __name__ == '__main__':
    main()
