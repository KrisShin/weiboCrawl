import pymysql


class DBDriver(object):
    '''
    mysql驱动
    '''

    def __init__(self) -> None:
        super().__init__()

        self.db = pymysql.connect(
            host='localhost',
            port=3306,
            user='webuser',
            passwd='123456',
            db='weibo',
            charset='utf8'
        )

        self.cursor = self.db.cursor()

    def insert_topic(self, topic: dict):
        '''insert topic if topic not exisit otherwise hot add 1.'''
        sql_string = f'''select id,hot from topic where name='{topic["name"]}';'''
        with self.db.cursor() as cursor:
            cursor.execute(sql_string)
            resp = cursor.fetchall()
            id, hot = resp[0] if resp else (None, None)
            if id:
                try:
                    cursor.execute(
                        f'''update topic set hot={hot+1} where id = {id};''')
                    self.db.commit()
                except Exception as err:
                    self.db.rollback()
                    print(err)
                    raise Exception('update topic failed.')
            else:
                try:
                    cursor.execute(
                        f'''insert into topic(name, hot) values('{topic["name"]}',1);''')
                    self.db.commit()
                except Exception as err:
                    self.db.rollback()
                    print(err)
                    raise Exception('insert topic failed.')

    def insert_feed(self, feed: dict):
        keys = ','.join(feed.keys())
        values = ','.join(
            [str(v) if isinstance(v, int) else f"'{v}'" for v in feed.values()])

        sql_string = f"replace into feed({keys}) values({values});"
        with self.db.cursor() as cursor:
            try:
                cursor.execute(sql_string)
                self.db.commit()
            except Exception as err:
                self.db.rollback()
                print(err)
                raise Exception('insert feed failed')

    def insert_comment(self, comment: dict):
        keys = ','.join(comment.keys())
        values = ','.join(
            [str(v) if isinstance(v, int) else f"'{v}'" for v in comment.values()])

        sql_string = f"replace into comment({keys}) values({values});"
        with self.db.cursor() as cursor:
            try:
                cursor.execute(sql_string)
                self.db.commit()
            except Exception as err:
                self.db.rollback()
                print(err)
                raise Exception('insert comment failed')


if __name__ == "__main__":
    db = DBDriver()

    from random import randint
    from datetime import datetime

    for t_id in range(3):
        db.insert_topic({'name': f'topic {t_id+1}'})
        for f_id in range(3):
            f_id = str(randint(10000, 99999))
            db.insert_feed(
                {
                    'mid': f_id,
                    'topic_id': str(t_id+1),
                    'content': f'feed {randint(10000, 99999)} for topic {t_id}',
                    'forward_count': randint(99, 999),
                    'comment_count': randint(99, 999),
                    'like_count': randint(99, 999),
                    'publish_time': datetime.now(),
                }
            )
            for c_id in range(3):
                db.insert_comment({
                    'id':str(randint(1000, 9999)),
                    'feed_id': f_id,
                    'content':f'comment {c_id} of feed {f_id}',
                    'publish_time': datetime.now(),
                    'like_count': randint(99, 999),
                    'reply_count': randint(99, 999),
                    'reply_like': randint(99, 999),
                })
