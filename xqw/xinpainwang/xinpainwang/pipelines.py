# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class XinpainwangPipeline:

    def open_spider(self,spider):
        self.db = pymysql.connect(host='localhost',
                        port=3306,
                        user='root',
                        password='123456',
                        database='xinpianwang')
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        dt_name = item.dt_name
        if dt_name == 'shouye':
            sql = f'insert into {dt_name} values("{item["Video_id"]}","{item["Video_title"]}","{item["Video_thum"]}","{item["Video_class"]}","{item["Video_time"]}","{item["Video_url"]}") '
        elif dt_name == 'datail':
            sql = f'insert into {dt_name} values("{item["url"]}","{item["Video"]}","{item["Videos_class"]}","{item["playback"]}","{item["description"]}","{item["details_play"]}","{item["Thumbs"]}","{item["Video_id"]}","{item["Video_thum"]}","{item["Video_url"]}","{item["author_url"]}")'
        elif dt_name == 'author_zy':
            sql = f'insert into {dt_name} values("{item["author_id"]}","{item["author_banner"]}","{item["author_avatar"]}","{item["author_name"]}","{item["author_introduce"]}","{item["author_new"]}","{item["author_fans"]}","{item["author_followers"]}","{item["author_Location"]}","{item["author_occupation"]}","{item["author_url"]}")'
        elif dt_name =='comment':
            sql = f'insert into {dt_name} values("{item["comment_id"]}","{item["resource_id"]}","{item["user_id"]}","{item["user_name"]}","{item["addtime"]}","{item["content"]}","{item["count_approve"]}")'
        # 执行sql语句
        try:
            self.cur.execute(sql)
            self.db.commit()
        except Exception as e:
            print('插入失败：', e)
        else:
            print(f'---------插入{dt_name}表成功----------')
        return item
    def close_spider(self, spider):
        pass
        self.cur.close()
        self.db.close()
