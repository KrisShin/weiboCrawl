import pymysql

class DBDriver(object):
    '''
    mysql驱动
    '''

    def __init__(self) -> None:
        '''
        初始化数据库连接
        '''
        super().__init__()

        self.db = pymysql.connect(
            host='localhost',
            port=3306,
            user='webuser',
            passwd='123456',
            db='weibo',
            charset='utf8mb4'
        )

    def insert_topic(self, topic: dict):
        '''如果topic不存在, 则插入一条新的topic, 存在则热度+1'''

        sql_string = f'''select id,hot from topic where name='{topic["name"]}';'''
        with self.db.cursor() as cursor:
            # 搜索当前topic是否存在
            cursor.execute(sql_string)
            resp = cursor.fetchall()
            id, hot = resp[0] if resp else (None, None)
            if id:
                try:
                    # topic的hot + 1
                    cursor.execute(
                        f'''update topic set hot={hot+1} where id = {id};''')
                    self.db.commit()
                    return id
                except Exception as err:
                    # 如果插入失败则回滚
                    self.db.rollback()
                    print(err)
                    raise Exception('update topic failed.')
            else:
                try:
                    # 新增一条topic
                    cursor.execute(
                        f'''insert into topic(name, hot) values('{topic["name"]}',1);''')
                    # 获取最新一条topic的id用于返回
                    last_id = cursor.lastrowid
                    self.db.commit()
                    return last_id
                except Exception as err:
                    self.db.rollback()
                    print(err)
                    raise Exception('insert topic failed.')

    def insert_feed(self, feed: dict, topic_id_list):
        '''插入feed, 和关联关系到数据库, 如果feed已存在则更新所有属性'''

        # 获取爬虫取出的所有属性
        keys = ','.join(feed.keys())
        values = []
        for val in feed.values():
            # 拼接sql语句 如果是数值 则转换为字符串类型, 否则强制转换为字符串类型, 并在两端加上单引号
            if isinstance(val, str):
                values.append(rf"'{val}'")
            elif isinstance(val, list) or isinstance(val,dict):
                # 将内容中原本的单引号全部替换为双引号, 因为单引号会导致sql执行报错
                values.append(r"'{}'".format(str(val).replace("'",'"')))
            elif isinstance(val, int):
                values.append(str(val))
            else:
                raise Exception('unsupport data type', type(val), val)

        update_keys = []
        for key in feed.keys():
            '''拼接更新语句, 排除mid, 主键不可更新'''
            if key=='mid':
                continue
            update_keys.append(f"""{key}=VALUES({key})""")

        # sql_string = f"""insert ignore into feed() values({','.join(values)});"""
        sql_string = f"""INSERT INTO feed({keys}) values({','.join(values)}) ON DUPLICATE KEY UPDATE {','.join(update_keys)};"""
        with self.db.cursor() as cursor:
            last_id = None
            try:
                # 替换sql语句中所有的转义字符\, \会导致sql执行报错
                cursor.execute(sql_string.replace(r"\'", r"'"))
                last_id = cursor.lastrowid
                self.db.commit()
            except Exception as err:
                self.db.rollback()
                print(err)
                raise Exception('insert feed failed')
            try:
                # 更新feed与topic的中间关系表
                tid_str_list=[]
                # 拼接sql
                for tid in topic_id_list:
                    tid_str_list.append(f"""('{tid}', '{feed["mid"]}')""")
                sql_string_relationship = f"""insert ignore into rs_topic_feed(topic_id, feed_mid) VALUES{','.join(tid_str_list)};"""
                cursor.execute(sql_string_relationship)
                self.db.commit()
            except Exception:
                pass
            return last_id

    def insert_comment(self, comment: dict):
        '''插入comment, 如果已存在则更新所有属性'''

        # 拼接sql
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
    # 以下是测试DBDriver工具类的代码
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
