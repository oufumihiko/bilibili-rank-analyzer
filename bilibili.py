import requests
from lxml import etree
import json
from bvtest import dec
import os
import datetime
import math

datenow = datetime.datetime.today().strftime('%Y-%m-%d') 
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}
proxy = '127.0.0.1:7890'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}


def getAllMemberVideo(mid,save="n") -> list:
    url = f'https://api.bilibili.com/x/space/arc/search?mid={mid}'
    #获取用户空间视频页数
    videoCount = requests.get(url=url,headers=headers).json()['data']['page']['count']
    pageSize = math.ceil(int(videoCount)/30)
    videoList = []
    for page in range(1,pageSize+1):
        url = f'https://api.bilibili.com/x/space/arc/search?mid={mid}&pn={page}'
        # print(url)
        page_n = requests.get(url=url,headers=headers).json()['data']['list']['vlist']
        videoList.append(page_n)
    if save == "y":
        with open(f'./{mid}.json','w',encoding='utf-8') as f:
            json.dump(videoList,fp=f,ensure_ascii=False)
    return videoList

def getTags(aid) -> list: #获取 Tag
    url = f'https://api.bilibili.com/x/web-interface/view/detail/tag?aid={aid}'
    tags = requests.get(url=url).json()['data']
    tagNames = []
    try:
        for tag in tags:
            tagNames.append(tag['tag_name'])
        return tagNames
    except:
        print("获取 Tag 失败.")

def getVideoInfo(bvid) -> dict:
    aid = str(dec(bvid)) #转换 bv 至 av
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

def getRank(save=1, saving_type=0):
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
    #分别获取各个榜单详情
    for ranking in rankings:
        try:
            print(f'正在获取{ranking}榜')
            url = rankings[ranking]
            response = requests.get(url=url,headers=headers).text
            tree = etree.HTML(response)
            ranklist = tree.xpath("//*[@id='app']/div[1]/div/div[1]/div[2]/div[3]/ul/li") 
            ranklistToSave = []
            for list in ranklist:
                num = list.xpath("./div[1]/text()")[0]
                title = list.xpath('./div[2]/div[2]/a/text()')[0]
                bvid = list.xpath('./div[2]/div[1]/a/@href')[0].lstrip('https://www.bilibili.com/video/')
                overall_score = list.xpath('./div[2]/div[2]/div[2]/div/text()')[0]
                video = {
                    'bvid' : bvid,
                    'num' : num,
                    'title' : title,
                    'overall_score' : overall_score
                }
                ranklistToSave.append(video)
            overallRanking[ranking] = ranklistToSave
            #持久化存储
            if not os.path.exists(f'./{datenow}'):
                os.makedirs(f'./{datenow}')
            if saving_type == 0:
                with open(f'./{datenow}/#总榜.json','w',encoding='utf-8') as f:
                    json.dump(overallRanking,fp=f,ensure_ascii=False)
            elif saving_type == 1:    
                with open(f'./{datenow}/{ranking}.json','w',encoding='utf-8') as f:
                    json.dump(ranklistToSave,fp=f,ensure_ascii=False)
            
            print(f'{ranking}榜 保存成功')
        except:
            print('获取榜单失败')
        
        

getRank()
    # for content in ranklist:
    #     num = content.xpath("./div[1]/text()")[0]
    #     title = content.xpath('./div[2]/div[2]/a/text()')[0]
    #     bvid = content.xpath('./div[2]/div[1]/a/@href')[0].lstrip('https://www.bilibili.com/video/')
    #     author = content.xpath('./div[2]/div[2]/div/a//text()')[0]
    #     overall_score = content.xpath('./div[2]/div[2]/div[2]/div/text()')[0]
    #     print(num,title,author)
    #     video = {
    #         'title' : title,
    #         'author' : author,
    #         'bvid' : bvid,
    #         'overall_score' : overall_score
    #     }
    #     rank = {
    #         'num' : num,
    #         'ranking' : ranking
    #     }
    #     video['ranking'] = []
    #     video['ranking'].append(rank)
    #     video_list.append(video)

    #     # video_info = getVideoInfo(bvid)

    #     # video = dict( video_info, **video )
    #     # video['tags'] = getTags(video['aid'])
    #     # time.sleep(5)
# with open('./ranking.json','w',encoding='utf-8') as f:
#     json.dump(video_list,fp=f,ensure_ascii=False)

