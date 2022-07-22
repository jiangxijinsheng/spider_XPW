import requests
import scrapy
from ..items import *
import json

class MyxinpianwangSpider(scrapy.Spider):
    name = 'myxinpianwang'
    allowed_domains = ['www.xinpianchang.com']
    start_urls = ['https://www.xinpianchang.com/channel/index/sort-like?from=navigator']
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                       ' Chrome/101.0.4951.67 Safari/537.36')
    }

    def parse(self, response,**kwargs):
        pass
        # print(response)
        li_list = response.xpath('//ul[@class="video-list"]/li')
        # print(len(li_list))
        for li in li_list:
            Video_id = li.xpath('./@data-articleid').get()  #视频id
            Video_title = li.xpath('./div/div/a/p/text()') .get() #视频标题
            Video_thum = li.xpath('./a/img/@src').get()  #视频缩略图
            Video_class = li.xpath('./div/div/div[1]/span[1][@class="fs_12 fw_300 c_b_9"]/text()').get() #视频分类
            Video_time = li.xpath('./a/div[2]/p/text()').get()  #视频创建时间
            Video_url = f'https://www.xinpianchang.com/a{Video_id}?from=ArticleList' #视频详情链接
            # print(Video_url)

            yield XinpainwangItem(Video_id=Video_url,
                                  Video_title=Video_title,
                                  Video_thum=Video_thum,
                                  Video_class=Video_class,
                                  Video_time=Video_time,
                                  Video_url=Video_url)
            request = scrapy.Request(
                # 访问视频详情
                url=Video_url,
                # 回调解析详情的函数
                callback=self.Video_detail,
                meta={'Video_id':Video_id,'Video_thum':Video_thum,'Video_url':Video_url}
            )
            yield request



    def Video_detail(self,response):
        Video_id = response.meta['Video_id']
        Video_thum = response.meta['Video_thum']
        Video_url = response.meta['Video_url']
        # print(Video_id)
        mid = response.xpath('//div[@class="filmplay-data-btn fs_12"]/span[2]/span[1]/a/@data-vid').get()

        url = f'https://mod-api.xinpianchang.com/mod/api/v2/media/{mid}?appKey=61a2f329348b3bf77&extend=userInfo%2CuserStatus'
        # print(url)
        content = requests.get(url=url).json()['data']
        # print(content)
        Video = content['resource']['progressive'][0]['url']  #视频格式
        # print(Video)
        Videos_class = content['categories']
        # print(Videos_class)
        playback = content['duration']
        # print(playback)
        description = content['description']
        # print(description)
        details_play = response.xpath('//div[@class="filmplay-data-play filmplay-data-info" ]/i/text()').get().replace(',','')
        # print(details_play)
        Thumbs = response.xpath('//div[@class="filmplay-data"]/div/span/span/span[@class="v-center like-counts fs_12 c_w_f fw_300 show"]/@data-counts').get()
        # print(Thumbs)
        li_list = response.xpath('//div[@class="filmplay-creator right-section"]/ul[@class="creator-list"]/li')
        for li in li_list:
            author_url = li.xpath('./a/@href').get()
            author_url = f'https://www.xinpianchang.com{author_url}'
        # print(author_url)
            yield xinqianwangdetailTtem(url=url,
                                        Video=Video,
                                        Videos_class=Videos_class,
                                        playback=playback,
                                        description=description,
                                        details_play=details_play,
                                        Thumbs=Thumbs,
                                        Video_id=Video_id,
                                        Video_thum=Video_thum,
                                        Video_url=Video_url,
                                        author_url=author_url
                                        )
            request = scrapy.Request(
        # 访问视频详情
                url=author_url,
                # 回调解析详情的函数
                callback=self.author_parse,
                meta={'author_url':author_url,'Video_id':Video_id,'Video_url':Video_url}
            )
            yield request

        comment_url = f'https://app2.xinpianchang.com/comments?resource_id={Video_id}&type=article&page=1&per_page=24'
        requset = scrapy.Request(
            url=comment_url,
            callback=self.comments_parse,
            dont_filter=True,
            meta={'Video_id': Video_id})
        yield requset

    def author_parse(self,response,**kwargs):
        # print(response)
        Video_url = response.meta['Video_url']
        # print(Video_url)
        Video_id = response.meta['Video_id']
        # print(Video_id)
        author_url=response.meta['author_url']
        # print(author_url)
        # print(1)
    #     author_url=f'https://www.xinpianchang.com/{author_id}'
    #     print(author_url)
        author_id = response.xpath('//div[@class="creator-info-wrap"]/div/div/a[3]/@data-userid').get()
        #图片
        author_banner=response.xpath('//div[@class="banner-wrap"]/@style').get()
        # print(author_banner)
        #头像
        author_avatar = response.xpath('//div[@class="banner-linear"]/span[@class="avator-wrap-s"]/img/@src').get()
        # print(author_avatar)
        #名称
        author_name = response.xpath('//div[@class="creator-info"]/p[@class="creator-name fw_600 c_b_26"]/span/text()').get()
        #自我介绍
        author_introduce = response.xpath('//div[@class="creator-info"]/p[@class="creator-desc fs_14 fw_300 c_b_3 line-hide-1"]/text()').get()
        #被点赞次数
        author_new = response.xpath('//span[@class="like-counts fw_600 v-center"]/text()').get()
        #粉丝数量
        author_fans = response.xpath('//span[@class="fans-counts fw_600 v-center"]/text()').get()
        #关注数量
        author_followers = response.xpath('//span[@class="fw_600 v-center"]/text()').get()
        # 所在位置
        author_Location = response.xpath('//p[@class="creator-detail fs_14 fw_300 c_b_9"]/span[@class="v-center"][1]/text()').get()
        # 职业
        author_occupation = response.xpath('//p[@class="creator-detail fs_14 fw_300 c_b_9"]/span[@class="v-center"][2]/text()').get()
        # print(author_occupation)

        yield xinqianwanauthorTtem( author_id=author_id,
                                    author_banner=author_banner,
                                    author_avatar=author_avatar,
                                    author_name=author_name,
                                    author_introduce=author_introduce,
                                    author_new=author_new,
                                    author_fans=author_fans,
                                    author_followers=author_followers,
                                    author_Location=author_Location,
                                    author_occupation=author_occupation,
                                    author_url=author_url,
                                    )


    def comments_parse(self, response):
        # print(response)
        li_list = response.json()['data']['list']
        for li in li_list:
            # 评论id
            comment_id = li['userInfo']['id']
            # 评论作品id（视频id）
            resource_id = li['resource_id']
            # 评论人id
            user_id = li['userid']
            # 评论人名称
            user_name = li['userInfo']['username']
            # 发表时间
            addtime = li['addtime']
            # 评论内容
            content = li['content']
            # 被点赞次数
            count_approve = li['count_approve']
            # print(count_approve)
            yield CommentItem(comment_id=comment_id, resource_id=resource_id,
                              user_id=user_id, user_name=user_name,
                              addtime=addtime, content=content,
                              count_approve=count_approve)
