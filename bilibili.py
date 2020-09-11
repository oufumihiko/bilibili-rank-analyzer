import requests, json, os, datetime, math
from lxml import etree
from bvtest import dec
import time

# 获取今日日期
datenow = datetime.datetime.today().strftime('%Y-%m-%d') 
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}

# 设置代理
proxy = '127.0.0.1:7890'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}


class Bvideo:
    def __init__(self, bvid):
        self.bvid = bvid
        self.blink = f'https://www.bilibili.com/video/{self.bvid}'
    
    def getAid(self):# 把bv号转换为av号
        self.aid = str(dec(self.bvid))


    def get_video_page(self):# 获取视频页面的文本形式并且返回
        video_page = requests.get(url=self.blink,headers=headers).text
        return video_page
    
    def getTags(self) -> list: # 获取 Tag 列表
        self.getAid()
        self.taglink = f'https://api.bilibili.com/x/web-interface/view/detail/tag?aid={self.aid}'

        tags = requests.get(url=self.taglink).json()['data']
        tagNames = []
        try:
            for tag in tags:
                tagNames.append(tag['tag_name'])
            return tagNames
        except:
            print("获取 Tag 失败.")

    def getThumbnailUrl(bvid): # 获取视频封面的地址
        page = requests.get(url=f'https://www.bilibili.com/video/{bvid}',headers=headers).text
        tree = etree.HTML(page)
        url = tree.xpath('//meta[@itemprop="thumbnailUrl"]/@content')[0]
        return url

def getAllMemberVideo(mid,save:bool= False, save_as_folder:bool= False) -> list: # 获取用户视频空间下所有视频
    url = f'https://api.bilibili.com/x/space/arc/search?mid={mid}'
    # 获取用户空间视频页数
    videoCount = requests.get(url=url,headers=headers).json()['data']['page']['count']
    pageSize = math.ceil(int(videoCount)/30)
    # 将空间下每一分页的信息储存到 videoList 之中
    videoList = []
    for page in range(1,pageSize+1):
        url = f'https://api.bilibili.com/x/space/arc/search?mid={mid}&pn={page}'
        page_n = requests.get(url=url,headers=headers).json()['data']['list']['vlist']
        videoList.extend(page_n)
    if save == True: # 储存开启时，保存到 "用户id.json"
        if save_as_folder == False:
            with open(f'./{mid}.json','w',encoding='utf-8') as f:
                json.dump(videoList,fp=f,ensure_ascii=False)
        else:
            with open(f'./{mid}/{mid}.json','w',encoding='utf-8') as f:
                json.dump(videoList,fp=f,ensure_ascii=False)
    return videoList

def getVideoInfo(bvid) -> dict: # 获取单个视频的播放、点赞、弹幕、回复、收藏、投币、分享数据
    aid = str(dec(bvid)) # 转换 bv 至 av
    try: 
        urljson = f'https://api.bilibili.com/x/web-interface/archive/stat?aid={aid}'
        video_info = requests.get(url=urljson,headers=headers,proxies=proxies).json()['data']
        del video_info["now_rank"]
        del video_info["his_rank"]
        del video_info["no_reprint"]
        del video_info["copyright"]
        del video_info["argue_msg"]
        del video_info["evaluation"]
        video_info['aid'] = aid
        #{'aid': '', 'bvid': '', 'view': , 'danmaku': , 'reply': , 'favorite': , 'coin': , 'share': , 'like': }
        return video_info
    except:
        print("获取视频信息失败.")

def getRank(save_to_file:bool = True, save_as_seperate_score:bool = False):  # 获取排行榜数据
    rankings = {
        '全站' : 'https://www.bilibili.com/ranking/all/0/0/3',
        '动画' : 'https://www.bilibili.com/ranking/all/1/0/3',
        '国创相关' : 'https://www.bilibili.com/ranking/all/168/0/3',
        '音乐' : 'https://www.bilibili.com/ranking/all/3/0/3',
        '舞蹈' : 'https://www.bilibili.com/ranking/all/129/0/3',
        '游戏' : 'https://www.bilibili.com/ranking/all/4/0/3',
        '知识' : 'https://www.bilibili.com/ranking/all/36/0/3',
        '数码' : 'https://www.bilibili.com/ranking/all/188/0/3',
        '生活' : 'https://www.bilibili.com/ranking/all/160/0/3',
        '美食' : 'https://www.bilibili.com/ranking/all/211/0/3',
        '鬼畜' : 'https://www.bilibili.com/ranking/all/119/0/3',
        '时尚' : 'https://www.bilibili.com/ranking/all/155/0/3',
        '娱乐' : 'https://www.bilibili.com/ranking/all/5/0/3',
        '影视' : 'https://www.bilibili.com/ranking/all/181/0/3'
    }
    overallRanking = {}
    # 分别获取各个榜单详情
    for ranking in rankings:
        try:
            print(f'- 正在获取{ranking}榜')
            # 从字典中读取对应排行榜链接并获取页面文本，使用xpath解析
            url = rankings[ranking]
            response = requests.get(url=url,headers=headers).text
            tree = etree.HTML(response)

            # 榜单中的视频排名数据
            ranklist = tree.xpath("//*[@id='app']/div[1]/div/div[1]/div[2]/div[3]/ul/li")
            ranklistToSave = [] # 用来保存
            for list in ranklist: # 遍历单个榜单中视频
                rank = list.xpath("./div[1]/text()")[0] # 排名
                title = list.xpath('./div[2]/div[2]/a/text()')[0] # 视频标题
                bvid = list.xpath('./div[2]/div[1]/a/@href')[0].lstrip('https://www.bilibili.com/video/') # bv号
                overall_score = list.xpath('./div[2]/div[2]/div[2]/div/text()')[0] # 综合得分
                video = {
                    'bvid' : bvid,
                    'rank' : rank,
                    'title' : title,
                    'overall_score' : overall_score,
                    'tags' : ''
                }
                ranklistToSave.append(video)
            overallRanking[ranking] = ranklistToSave # 储存分排行榜至 overallRanking
            
            # 持久化存储
            if save_to_file == True and save_as_seperate_score == True:
                if not os.path.exists(f'./{datenow}'):
                    os.makedirs(f'./{datenow}')  
                with open(f'./{datenow}/{ranking}.json','w',encoding='utf-8') as f:
                    json.dump(ranklistToSave,fp=f,ensure_ascii=False)
                    print(f'√ {ranking}榜 保存成功')
        except:
            print('× 获取榜单失败')

    if save_to_file == True:
        if not os.path.exists(f'./{datenow}'):
                    os.makedirs(f'./{datenow}')
        with open(f'./{datenow}/#总榜.json','w',encoding='utf-8') as fp:
            json.dump(overallRanking,fp=fp,ensure_ascii=False)
            print(f'√ 总榜 保存成功')
    
    return overallRanking
    


if __name__ == "__main__":
    while True:
        os.system("cls")
        print("=============== bilibili rank analyzer ===============")
        print()
        print("         0. Get today's rank on bilibili.")
        print("         1. Crawl tags for the rank list.")
        print("         2. Crawl user's playlist & thumbnail")
        print()
        print("======================================================")
        input_selection = input("Type a number: ")
        if input_selection == '0':
            rank_list = getRank(save_to_file=True, save_as_seperate_score=False)
            continue
        if input_selection == '1':
            for rank in rank_list:
                for video in rank_list[rank]:
                    target_video = Bvideo(video['bvid'])
                    try:
                        video['tags'] = target_video.getTags()
                    except:
                        print(f"获取{video['bvid']} 标签失败！")
                    print(video['title'],video['bvid'],video['tags'])
                    time.sleep(1)
        if input_selection == '2':
            # mid = 93415
            os.system("cls")
            print("==================== User Space ====================")
            mid = input('Type user id you want to crawl: ')
            getAllMemberVideo(mid,save=True, save_as_folder=True)
            with open(f'./{mid}/{mid}.json', 'r', encoding='utf-8') as f:
                vlist = json.load(fp=f)
                count = len(vlist)
                print(f'共 {len(vlist)} 个封面待下载')
                i = 1
                for v in vlist:
                    bvid = v['bvid']
                    link = 'http:' + v['pic']
                    ftype = v['pic'].split('.')[-1] # 文件格式
                    pic = requests.get(url = link).content
                    print(f'正在下载第 {i} 个封面，剩余 {count-i} 个')
                    if not os.path.exists(f'./{mid}'):
                            os.makedirs(f'./{mid}')
                    with open(f'./{mid}/{bvid}.{ftype}','wb') as img:
                        img.write(pic)
                    i += 1


