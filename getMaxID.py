import re
import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
	url = 'http://www.bilibili.com/newlist.html'
	tmp = requests.get(url=url)
	html = BeautifulSoup(tmp.text, 'lxml')
	maxid = html.select('li[class=l1]')[0].a.attrs['href'].replace('/video/av', '').replace('/', '')
	print(int(maxid))
