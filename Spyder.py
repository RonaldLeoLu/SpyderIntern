#!python3
#-*- conding:utf-8 -*-
import requests
from requests.exceptions import RequestException
import re
import pymongo
from config import *

client = pymongo.MongoClient(Mongo_URL)
db = client[Mongo_DB]

def get_url(a='python',b='上海',i=1):
	return 'http://www.shixiseng.com/interns?k={0}+{1}&p={2}'.format(a,b,i)

def get_page_number(html):
	pattern = re.compile('<li.*?title="第.*?共(\d+)页.*?>',re.S)
	items = re.findall(pattern,html)
	return int(items[0])


def get_one_page(url):
	try:
		response = requests.get(url)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		return None

def parse_one_page(html):
	pattern = re.compile('<div class="list".*?class="names">.*?<a href=.*?target="_blank">(.*?)</a>'
						+'.*?<div class="part".*?<a href=.*?target="_blank">(.*?)</a>'
						+'.*?<span>.*?<i class="money"></i>(.*?)</span>'
						+'.*?<img src.*?span>(.*?)</span.*?class="line">'
						+'.*?<img src.*?span>(.*?)</span>',re.S)
	items = re.findall(pattern, html)
	for item in items:
		yield{
			'职位':item[0],
			'公司':item[1],
			'薪酬':item[2].strip(),
			'天数':item[3],
			'持续':item[4]
		}

def save_to_mongo(result):
	try:
		if db[Mongo_TABLE].insert(result):
			print('成功存储到Mongo', result)
	except Exception:
		print('存储到mongo失败')

def main():
	url = get_url(i=1)
	html = get_one_page(url)
	number = get_page_number(html)
	for i in range(1,number):
		url = get_url(i=i)
		html = get_one_page(url)
		for item in parse_one_page(html):
			save_to_mongo(item)
	
if __name__ == '__main__':
	main()
