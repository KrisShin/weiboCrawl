import pymysql
import json


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
            charset='utf8mb4'
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
                    last_id = cursor.lastrowid
                    self.db.commit()
                    return last_id
                except Exception as err:
                    self.db.rollback()
                    print(err)
                    raise Exception('update topic failed.')
            else:
                try:
                    cursor.execute(
                        f'''insert into topic(name, hot) values('{topic["name"]}',1);''')
                    last_id = cursor.lastrowid
                    self.db.commit()
                    return last_id
                except Exception as err:
                    self.db.rollback()
                    print(err)
                    raise Exception('insert topic failed.')

    def insert_feed(self, feed: dict, topic_id_list):
        keys = ','.join(feed.keys())
        values = []
        for val in feed.values():
            if isinstance(val, str):
                values.append(rf"'{val}'")
            elif isinstance(val, list) or isinstance(val,dict):
                values.append(r"'{}'".format(str(val).replace("'",'"')))
            elif isinstance(val, int):
                values.append(str(val))
            else:
                raise Exception('unsupport data type', type(val), val)

        update_keys = []
        for key in feed.keys():
            if key=='mid':
                continue
            update_keys.append(f"""{key}=VALUES({key})""")

        # sql_string = f"""insert ignore into feed() values({','.join(values)});"""
        sql_string = f"""INSERT INTO feed({keys}) values({','.join(values)}) ON DUPLICATE KEY UPDATE {','.join(update_keys)};"""
        with self.db.cursor() as cursor:
            last_id = None
            try:
                cursor.execute(sql_string.replace(r"\'", r"'"))
                last_id = cursor.lastrowid
                self.db.commit()
            except Exception as err:
                self.db.rollback()
                print(err)
                raise Exception('insert feed failed')
            try:
                tid_str_list=[]
                for tid in topic_id_list:
                    tid_str_list.append(f"""('{tid}', '{feed["mid"]}')""")
                sql_string_relationship = f"""insert ignore into rs_topic_feed(topic_id, feed_mid) VALUES{','.join(tid_str_list)};"""
                cursor.execute(sql_string_relationship)
                self.db.commit()
            except Exception:
                pass
            return last_id

    def insert_comment(self, comment: dict):
        keys = ','.join(comment.keys())
        values = ','.join(
            [f"'{v}'" if isinstance(v, str) else str(v) for v in comment.values()])
        
        update_keys = []
        for key in comment.keys():
            if key=='id':
                continue
            update_keys.append(f"""{key}=VALUES({key})""")

        # sql_string = f"insert ignore into comment({keys}) values({values});"
        sql_string = f"""INSERT INTO comment({keys}) values({values}) ON DUPLICATE KEY UPDATE {','.join(update_keys)};"""
        with self.db.cursor() as cursor:
            try:
                cursor.execute(sql_string)
                last_id = cursor.lastrowid
                self.db.commit()
                return last_id
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
                    'id': str(randint(1000, 9999)),
                    'feed_id': f_id,
                    'content': f'comment {c_id} of feed {f_id}',
                    'publish_time': datetime.now(),
                    'like_count': randint(99, 999),
                    'reply_count': randint(99, 999),
                    'reply_like': randint(99, 999),
                })