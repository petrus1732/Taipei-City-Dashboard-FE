# from joblib import Parallel, delayed
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
import time

CHROME_DRIVER = "C:\Program Files\chromedriver-win64\chromedriver.exe"

options = Options()
options.add_experimental_option('excludeSwitches',['enable-logging'])
options.add_argument("--disable-notifications")
options.add_argument("--headless") #remove the comment for running without opening the web page
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")

d = webdriver.Chrome(service=Service(CHROME_DRIVER), options=options)
d.set_window_size(1440, 900)
d.get("https://ap.ece.moe.edu.tw/webecems/pubSearch.aspx")
select_element = d.find_element(By.ID, 'ddlCityS')
select = Select(select_element)
select.select_by_visible_text('臺北市')
d.find_element(By.ID, "btnSearch").click()
d.execute_script("window.scrollTo(0, 6000)") 
time.sleep(2)
page = 71
end = page + 3
d.find_element(By.ID, "PageControl1_txtPages").clear()
time.sleep(1)
d.find_element(By.ID, "PageControl1_txtPages").send_keys(str(page))
time.sleep(3)
d.find_element(By.ID, "PageControl1_lbPageChg").click()
time.sleep(3)
d.execute_script("window.scrollTo(0, 0)") 
time.sleep(1)
with open(f"kindergartens{page}.json", "w", encoding="utf-8") as f:
	while page != end:
		for i in range(10):
			print(d.find_element(By.ID, f"GridView1_btnMore_{i}").is_displayed())
			d.find_element(By.ID, f"GridView1_btnMore_{i}").click()
			time.sleep(0.9)
			suc = False
			while not suc:
				try:
					obj = {
						"name": d.find_element(By.ID, f"GridView1_lblSchName_{i}").text,
						"district": d.find_element(By.ID, f"GridView1_lblArea_{i}").text,
						"type": d.find_element(By.ID, f"GridView1_lblPub_{i}").text,
						"address": d.find_element(By.ID, f"GridView1_hlAddr_{i}").text,
						"telephone": d.find_element(By.ID, f"GridView1_lblTel_{i}").text,
						"people": d.find_element(By.ID, f"GridView1_lblGenStd_{i}").text,
						"quasi-public":d.find_element(By.ID, f"GridView1_lblStdPub_{i}").text
					}
					suc = True
					for keys, value in obj.items():
						if len(value) == 0:
							suc = False
							break
				except Exception as e: print(e)
				time.sleep(1)
			print (obj)
			info = json.dumps(obj, ensure_ascii=False)
			f.write(info)
			f.write(',')
		print(f'page{page} done!')
		d.find_element(By.ID, "PageControl1_lbNextPage").click()
		page += 1
		time.sleep(5)
		suc = False
		while not suc:
			try:
				d.execute_script("window.scrollTo(0, 0)") 
				time.sleep(5)
				if d.find_element(By.ID, f"GridView1_btnMore_0").is_displayed():
					suc = True
				print("page turned and went back to the top!")
			except Exception as e: print(e)
			time.sleep(1)



