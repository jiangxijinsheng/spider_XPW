# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XinpainwangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    dt_name = 'shouye'
    Video_id = scrapy.Field()
    Video_title = scrapy.Field()
    Video_thum = scrapy.Field()
    Video_class = scrapy.Field()
    Video_time = scrapy.Field()
    Video_url = scrapy.Field()

class xinqianwangdetailTtem(scrapy.Item):
    dt_name = 'datail'
    url = scrapy.Field()
    Video = scrapy.Field()
    Videos_class = scrapy.Field()
    playback = scrapy.Field()
    description = scrapy.Field()
    details_play = scrapy.Field()
    Thumbs = scrapy.Field()
    Video_id = scrapy.Field()
    Video_thum = scrapy.Field()
    Video_url = scrapy.Field()
    author_url = scrapy.Field()

class xinqianwanauthorTtem(scrapy.Item):
    dt_name = 'author_zy'
    author_id =scrapy.Field()
    author_banner =scrapy.Field()
    author_avatar =scrapy.Field()
    author_name =scrapy.Field()
    author_introduce =scrapy.Field()
    author_new =scrapy.Field()
    author_fans =scrapy.Field()
    author_followers =scrapy.Field()
    author_Location =scrapy.Field()
    author_occupation =scrapy.Field()
    author_url = scrapy.Field()

class CommentItem(scrapy.Item):
    dt_name='comment'
    comment_id = scrapy.Field()
    resource_id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    addtime = scrapy.Field()
    content = scrapy.Field()
    count_approve = scrapy.Field()
