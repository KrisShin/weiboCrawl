"""
微博 超话页面抓取
"""
import sys

import requests
import json
from datetime import datetime

from w3lib import html

from web.global_variable import db

from web.constriant import BASE_CRAWL_URL
from web.models import User, Weibo, WeiboText


class WeiBoSpider(object):
    def __init__(self):
        # 首页的url，翻页的url是通过since_id控制的，下一页的since_id可以在当前页的响应中获取
        self.url = BASE_CRAWL_URL
        self.count = 0

    def run(self, page_count):
        res = self.get_response(self.url)
        self.parse_data(res, page_count)

    def get_response(self, url):
        # 访问url，获取响应
        r = requests.get(url)
        # 访问完成之后，这里将响应源码存入数据库
        # wb_text表
        weibo_text = WeiboText(
            url=url, response_text=r.text, response_code=r.status_code
        )
        db.session.add(weibo_text)
        db.session.commit()
        return r.text

    def parse_data(self, response, page_count):
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
                user_id = card['mblog']['user']['id']
                # 昵称
                name = card['mblog']['user']['screen_name']
                # 头像
                head_photo = card['mblog']['user']['profile_image_url']
                # 发布时间
                timestamp_text = datetime.strptime(
                    card['mblog']['created_at'], '%a %b %d %H:%M:%S %z %Y'
                )
                # 评论数
                comments_count = card['mblog']['comments_count']
                # 点赞数
                attitudes_count = card['mblog']['attitudes_count']
                # 视频链接
                try:
                    mp4 = [card['mblog']['page_info']['urls']['mp4_720p_mp4']]
                    
                except KeyError:
                    mp4 = None
                # 如果正文有图片，则图片链接
                pic_links = None
                try:
                    all_link = card['mblog']['pics']
                    if all_link:
                        pic_links = [_['large']['url'] for _ in all_link]
                except KeyError:
                    pass

                user_obj = User.query.filter_by(id=user_id).first()
                if not user_obj:
                    user_obj = User(
                        id=user_id, username=name, avatar=head_photo, password='123456'
                    )
                    db.session.add(user_obj)
                weibo_obj = Weibo.query.filter_by(mid=mid).first()
                if not weibo_obj:
                    weibo_obj = Weibo(
                        user=user_obj,
                        mid=mid,
                        publish_time=timestamp_text,
                        from_chaohua='山西工商学院超话',
                        comment_count=comments_count,
                        video_list=mp4,
                        image_list=pic_links,
                        content=text,
                    )
                    db.session.add(weibo_obj)
                weibo_obj.like_count = attitudes_count
                weibo_obj.comment_count = comments_count
                db.session.commit()
                self.count += 1
                sys.stdout.write('\rCrawling: {}'.format(self.count))
        if page_count < 0:
            return
        # 访问下一页
        try:
            since_id = json_result['data']['pageInfo']['since_id']
            # 下一页的url
            next_url = self.url + f'&since_id={since_id}'
            next_res = self.get_response(next_url)
            self.parse_data(next_res, page_count - 1)
        except KeyError:
            # 结束，关闭数据库连接
            self.cursor.close()
            self.driver.db.close()


if __name__ == '__main__':
    WeiBoSpider().run()
