import requests,json
import math

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}

def getAllMemberVideo(mid):
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
        
    with open(f'./{mid}.json','w',encoding='utf-8') as f:
        json.dump(videoList,fp=f,ensure_ascii=False)