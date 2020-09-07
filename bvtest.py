#https://gist.githubusercontent.com/abc1763613206/b8afbb88849835f064f74e652fdb16c5/raw/1f60c45c7286d5d5ab522d214e9f9bd051477c2a/bvtest.py
import requests
import json
import random


Back_URL = 'https://api.bilibili.com/x/web-interface/archive/stat?aid='

headers = {
	'Cookie': "Replace Me With REAL COOKIE" ,
	'Pragma': 'no-cache',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr={}
for i in range(58):
	tr[table[i]]=i
s=[11,10,3,8,4,6]
xor=177451812
add=8728348608

def dec(x):
	r=0
	for i in range(6):
		r+=tr[x[s[i]]]*58**i
	return (r-add)^xor

def enc(x):
	x=(x^xor)+add
	r=list('BV1  4 1 7  ')
	for i in range(6):
		r[s[i]]=table[x//58**i%58]
	return ''.join(r)


def checkv(x,y):
	if str(enc(int(x))) == str(y):
		return "Vaild √"
	else:
		return "Not Vaild ×"

# for i in range(0,50000):
# 	n = random.randint(100,9999999)
# 	resp = requests.get(Back_URL+str(n),headers=headers)
# 	#print(resp.text)
# 	res = json.loads(resp.text)
# 	if int(res["code"]==0):
# 		print("{} {} {}".format(res["data"]["aid"],res["data"]["bvid"],str(checkv(res["data"]["aid"],res["data"]["bvid"]))))

