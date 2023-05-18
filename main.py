from bs4 import BeautifulSoup
import requests
import sys
import traceback
import json
import os
from decouple import config

URL = config("URL")

with open('./farm.json', 'r') as file:
    content = json.load(file)
s = requests.Session()
def run():
	response = s.get(URL)
	response.encoding="utf-8"
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
			print(today)
			content['data'].append(today)
			with open(os.path.join('./farm.json'), 'w') as f_new:
				json.dump(content, f_new, ensure_ascii=False)
		print('tr not found')
	print('插入data完成')
def main():
	run()
if __name__ == '__main__':
	try:
		sys.exit(main())
	except Exception as e:
		traceback.print_exc()