from bs4 import BeautifulSoup
import requests
import sys
import traceback
import json
import os
from decouple import config

URL = config("URL")

content = {
	'data': []
}
s = requests.Session()
def run():
	response = s.get(URL)
	response.encoding="utf-8"
	if response.status_code == 200:
		bs = BeautifulSoup(response.text, 'html.parser')
		contentbox = bs.find("div", "content")
		table = contentbox.find("table").find('table')
		trs = table.find_all("tr")
		content['data'] = []
		print('清空data')
		for tr in trs:
			if tr:
				tds = tr.find_all("td")
				if tds[0].get_text().strip() == "日期":
					continue
				today = {
					"date": tds[0].get_text().strip(),
					"question": tds[1].get_text().strip(),
					"answer": tds[2].get_text().strip()
				}
				content['data'].append(today)
		with open(os.path.join('./farm.json'), 'w') as f_new:
			json.dump(content, f_new, ensure_ascii=False)
		print('插入data完成')
	else:
		print('请求失败')
def getTodayData():
	response = s.get("http://m.bzqm8.com/sy9321.html")
	response.encoding="utf-8"
	if response.status_code == 200:
		bs = BeautifulSoup(response.text, 'html.parser')
		articleDes = bs.find("section", "article_des")
		fisrtP = articleDes.p
		nextP = fisrtP.next_sibling
		print(fisrtP.get_text())
		print(nextP.get_text())
		s.post("https://thor.emoz.top/ant/insert.php", '', {
			'data': [fisrtP.get_text(), nextP.get_text()]
		})
	else:
		print('请求失败')
def main():
	run()
	getTodayData()
if __name__ == '__main__':
	try:
		sys.exit(main())
	except Exception as e:
		traceback.print_exc()