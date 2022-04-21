"""
微博 超话页面抓取
"""
import sys

import requests
import json
import pymysql

from w3lib import html


class WeiBo(object):

    def __init__(self):
        # 首页的url，翻页的url是通过since_id控制的，下一页的since_id可以在当前页的响应中获取
        self.url = 'https://m.weibo.cn/api/container/getIndex?containerid=1008088f7809e2286a4cbd0e5aa8a352ffbca6&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%B1%B1%E8%A5%BF%E5%B7%A5%E5%95%86%E5%AD%A6%E9%99%A2'
        self.count = 0
        self.coon = pymysql.connect(
            host='101.34.234.17',
            port=3306,
            user='webuser',
            password='123456',
            database='weibo',
            charset='utf8'
        )
        self.cursor = self.coon.cursor()

    def run(self):
        res = self.get_response(self.url)
        self.parse_data(res)

    def get_response(self, my_url):
        # 访问url，获取响应
        r = requests.get(my_url)
        # 访问完成之后，这里将响应源码存入数据库
        # wb_text表
        sql = "insert ignore into wb_text (url, response_text, response_code) values (%s, %s, %s);"
        self.cursor.execute(sql, [my_url, r.text, "200"])
        self.coon.commit()
        return r.text

    def parse_data(self, response):
        # 解析数据
        json_result = json.loads(response)
        # 解析该页数据
        datas = json_result['data']['cards']
        for data in datas:
            if 'card_group' not in data.keys():
                continue
            for card in data['card_group']:
                if 'mblog' not in card.keys():
                    continue
                # mid
                mid = card['mblog']['mid']
                card_text = card['mblog']['text']
                # 正文内容
                text = html.remove_tags(card_text).strip('山西工商学院').strip()
                # 昵称
                name = card['mblog']['user']['screen_name']
                # 头像
                head_photo = card['mblog']['user']['profile_image_url']
                # 发布时间
                timestamp_text = ' '.join(card['mblog']['created_at'].split()[:-2])
                # 评论数
                comments_count = card['mblog']['comments_count']
                # 点赞数
                attitudes_count = card['mblog']['attitudes_count']
                # 视频链接
                try:
                    mp4 = json.dumps([card['mblog']['page_info']['urls']['mp4_720p_mp4']])
                except KeyError:
                    mp4 = None
                # 如果正文有图片，则图片链接
                pic_links = None
                try:
                    all_link = card['mblog']['pics']
                    if all_link:
                        pic_links = json.dumps([_['large']['url'] for _ in all_link])
                except KeyError:
                    pass

                # wb_user表
                sql_1 = 'insert ignore into wb_user (username, avatar, password) values (%s, %s, %s);'
                # wb_weibo表
                sql_2 = 'insert ignorey100 into wb_weibo (user_id, mid, publish_time, from_chaohua, comment_count, like_count, content, video_list, image_list) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
                self.cursor.execute(sql_1, [name, head_photo, '123456'])
                # user_id
                user_id = str(self.cursor.lastrowid)
                self.cursor.execute(sql_2,
                                    [user_id, mid, timestamp_text, '山西工商学院超话', comments_count, attitudes_count, text,
                                     mp4, pic_links])
                self.coon.commit()
                self.count += 1
                sys.stdout.write('\rCrawling: {}'.format(self.count))
        # 访问下一页
        try:
            since_id = json_result['data']['pageInfo']['since_id']
            # 下一页的url
            next_url = self.url + f'&since_id={since_id}'
            next_res = self.get_response(next_url)
            self.parse_data(next_res)
        except KeyError:
            # 结束，关闭数据库连接
            self.coon.close()
            self.cursor.close()


if __name__ == '__main__':
    WeiBo().run()
