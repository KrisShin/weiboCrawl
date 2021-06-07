from spiders.db_driver import DBDriver
from lxml import etree
import time
import requests
import json
import re
import pymongo
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# 设置 webdriver 无头运行
chrome_options.add_argument('--headless')
# 初始化 webdriver
driver = webdriver.Chrome(
    executable_path="./spiders/chromedriver/chromedriver_linux", chrome_options=chrome_options)
# driver = webdriver.Chrome(
#     executable_path="./spiders/chromedriver/chromedriver.exe", chrome_options=chrome_options)

# 屏蔽 https 证书报警信息
urllib3.disable_warnings()

# 定义 session  请求头，设置 UA
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}

# 定义异常数量全局变量
EXCEPTION_COUNT = 0
# 定义异常最大值全局变量
MAX_EXCEPTION_COUNT = 1000


class DBConn:
    conn = None
    servers = "mongodb://localhost:27017"

    def connect(self):
        self.conn = pymongo.MongoClient(self.servers)

    def close(self):
        return self.conn.disconnect()

    def get_conn(self):
        return self.conn


# 记录抓取异常
def record_exception_count():
    global EXCEPTION_COUNT
    EXCEPTION_COUNT += 1
    # 抓取异常次数达到最大值时抛出异常
    if EXCEPTION_COUNT > MAX_EXCEPTION_COUNT:
        print("exceed max exception count")
        raise RuntimeError


# 初始化 chromedriver 获取首页 cookie
def init_driver():
    driver.get("https://weibo.com/login.php?category=0")
    try:
        # 等待页面热点列表出现后再继续执行
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="UG_contents"]/ul/div//div[@class="list_des"]'))
        )
    except Exception:
        print("driver init failed")
        raise RuntimeError


# 获取首页 session，用于抓取首页热点列表信息
def get_weibo_session():
    s = requests.Session()
    resp = s.get(
        "https://weibo.com/login.php?category=0", headers=headers, verify=False)
    headers['refer'] = "https://weibo.com/login.php?category=0"
    if resp.status_code != 200:
        print("get weibo session failed")
        raise RuntimeError
    return s


# 通过 session 请求指定页的热点列表
def request_hot_list(s, page):
    path = "https://weibo.com/a/aj/transform/loadingmoreunlogin?ajwvr=6&category=0&page={}&lefnav=0&cursor=&__rnd={}".format(
        page, int(time.time()*1000))
    resp = s.get(
        path, headers=headers, verify=False)
    if resp.status_code != 200:
        # 记录请求页面异常
        return record_exception_count()
    data = json.loads(resp.text)
    return data.get('data', '')


# 解析首页热点列表链接
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


# 请求热点链接获取热点详情页 html 用于后续解析
def request_hot_detail(link):
    driver.get(link)
    try:
        # 等待热点评论节点出现后再继续执行，保证页面加载完整
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@node-type="root_comment"]'))
        )
        # 将页面滑动到最低端，加载更多评论信息
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
    except Exception as e:
        print(repr(e))
        # 记录请求页面异常
        return record_exception_count()
    return driver.page_source


# 格式化 xpath 解析的热点列表
def format_link_list(link_list):
    result = []
    for link in link_list:
        if link == "" or link in result:
            continue
        # 解析的页面可能没有 https 前缀，需要添加
        if not link.startswith("https:"):
            link = 'https:{}'.format(link)
        result.append(link)
    return result


# 格式化点赞数转发数等数字类型字符串，因为没有评论或点赞时会是对应的描述，因此需要特殊处理
def format_number(s):
    try:
        n = int(s)
        return n
    except ValueError:
        pass
    return 0


# 解析获取 @xxx 列表
def parse_at_name_list(selector):
    result = []
    # 获取相关标签列表
    at_name_tags = selector.xpath(
        '//div[@class="WB_detail"]//a[@extra-data="type=atname"]')
    for a in at_name_tags:
        result.append({
            "atName": ''.join(a.xpath('./text()')),
            "link": 'https:{}'.format(''.join(a.xpath('./@href')))
        })
    return result


# 使用 xpath 解析热点详情页面源码，生成存入数据库的数据
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
        "atNameList": parse_at_name_list(selector),
        "imageList": format_link_list(selector.xpath('//div[@class="WB_detail"]//img[not(@class="W_img_face")]/@src')),
        "videoList": format_link_list(selector.xpath('//div[@class="WB_detail"]//div[@class="media_box"]//video/@src')),
        "shareCount": format_number(''.join(selector.xpath('//div[@class="WB_handle"]/ul/li[2]//span[@class="line S_line1"]/span//em[2]/text()'))),
        "commentCount": format_number(''.join(selector.xpath('//div[@class="WB_handle"]/ul/li[3]//span[@class="line S_line1"]/span//em[2]/text()'))),
        "likeCount": format_number(''.join(selector.xpath('//div[@class="WB_handle"]/ul/li[4]//span[@class="line S_line1"]/span//em[2]/text()')))
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


# 解析评论
def parse_comments(html, mid):
    if not html:
        return None

    result = []
    selector = etree.HTML(html)
    comment_div_list = selector.xpath(
        '//div[@class="repeat_list"]/div[@node-type="feed_list"]/div[@class="list_box"]/div[@class="list_ul"]/div')
    for div in comment_div_list:
        comment_detail = {
            "mid": mid,
            "commentId": ''.join(div.xpath('./@comment_id')),
            "user": {
                "headPic": '{}'.format(''.join(div.xpath('./div[@class="WB_face W_fl"]/a/img/@src'))),
                "homepage": 'https:{}'.format(''.join(div.xpath('./div[@class="list_con"]/div[@class="WB_text"]/a[1]/@href'))),
                "nickname": ''.join(div.xpath('./div[@class="list_con"]/div[@class="WB_text"]/a[1]/text()'))
            },
            "contentList": div.xpath('./div[@class="list_con"]/div[@class="WB_text"]/text()'),
            "likeCount": format_number(''.join(div.xpath('./div[@class="list_con"]/div[@class="WB_func clearfix"]//span[@node-type="like_status"]/em[2]/text()'))),
            "replyCount":  format_number(''.join(re.findall(r'共(\d+)条回复', ''.join(div.xpath('.//div[@class="list_li_v2"]//a[@action-type="login"]/text()')))))
        }
        result.append(comment_detail)
    return result


def save_topic(db, topic_list):
    topic_id_list = []
    for topic in topic_list:
        # ''.strip(' \n\r')
        topic = topic.strip(' \n\r')
        if topic == "":
            continue
        t_id = db.insert_topic({'name': topic})
        topic_id_list.append(t_id)
    return topic_id_list


def format_str_list(origin):
    '''将列表拼接为字符串'''
    result = ''
    for s in origin:
        result = '{}|{}'.format(result, s)
    return result


def save_hot_detail(db, detail, topic_id_list):
    doc = {
        'mid': detail['mid'],
        'content': format_content(detail['contentList']),
        'forward_count': detail['shareCount'],
        'comment_count': detail['commentCount'],
        'like_count': detail['likeCount'],
        'publish_time': detail['publishTime'],
        'link': detail['link'],
        'from_dev': detail['from'],
        'at_names': [at['atName'] for at in detail['atNameList']],
        'image_list': detail['imageList'][:-1],  # 最后一张图片是用户头像, 所以排除掉
        'video_list': detail['videoList'],
        'topic_list': detail['topicList'],
        'user_avatar': detail['user']['headPic'],
        'user_homepage': detail['user']['homepage'],
        'user_name': detail['user']['nickname']
    }
    db.insert_feed(doc, topic_id_list)


def save_hot_comment(db, comments, mid):
    for comment in comments:
        doc = {
            'id': comment['commentId'],
            'feed_id': mid,
            'content': format_content(comment['contentList']),
            'like_count': comment['likeCount'],
            'reply_count': comment['replyCount'],
            'user_name': comment['user']['nickname'],
            'user_avatar': comment['user']['headPic'],
        }
        try:
            db.insert_comment(doc)
        except:
            pass


def format_content(content_list):
    result = ""
    for content in content_list:
        content = content.strip(' ')
        result = '{}{}'.format(result, content)
    return result


# 开始抓取
def crawl(total, conn, db):
    count = 0
    page = 1

    # 处理异常，用于正常关闭数据库连接和 webdriver
    try:
        # 初始化 webdriver
        init_driver()
        # 获取首页 session
        s = get_weibo_session()
        # 控制抓取数量
        while count < total:
            # 获取首页热点列表
            html = request_hot_list(s, page)
            if html == None:
                continue
            page += 1
            link_list = parse_hot_link(html)
            if not link_list:
                # 记录解析异常
                record_exception_count()
                continue
            for link in link_list:
                start_time = time.time()
                # 请求热点详情页
                detail_html = request_hot_detail(link)
                # 解析热点详情
                hot_detail = parse_hot_detail(detail_html, link)
                if not hot_detail or hot_detail.get('mid', '') == '':
                    # 解析数据异常，记录异常
                    record_exception_count()
                    continue
                count += 1
                # 热点话题存入数据库
                topic_ids = save_topic(db, hot_detail.get("topicList", []))
                # 热点详情存入数据库
                save_hot_detail(db, hot_detail, topic_ids)
                # 解析热点评论
                comments = parse_comments(detail_html, hot_detail['mid'])
                if len(comments) > 0:
                    # 热点评论存入数据库
                    save_hot_comment(db, comments, hot_detail['mid'])
                print(f'第{count}条数据爬取完成，链接: {link}，耗时: {time.time()-start_time}')
    except Exception as e:
        print(repr(e))
    finally:
        # 关闭数据库连接和 webdriver
        print("close db conn and webdriver")
        conn.close()
        driver.quit()
        # 重置异常设置，用于下次重新执行抓取
        EXCEPTION_COUNT = 0
        MAX_EXCEPTION_COUNT = 0
    return


def run_spider(total=10):
    db = DBConn()
    mysql_driver = DBDriver()
    db.connect()
    conn = db.get_conn()
    crawl(total, conn, mysql_driver)


if __name__ == '__main__':
    run_spider()
