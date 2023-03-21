from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
# opt = Options()
# opt.add_experimental_option("debuggerAddress","localhost:9222")
# driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe",chrome_options=opt)

PATH = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome(PATH)
link = "https://cyberconflicts.cyberpeaceinstitute.org/threats/attack-details"
driver = ""

def launchBrowser():
	chrome_options = Options()
	# chrome_options.binary_location=PATH
	chrome_options.add_argument("disable-infobars");
	driver = webdriver.Chrome(executable_path=PATH, chrome_options=chrome_options)

	driver.get(link)
	# driver.find_element(By.CLASS_NAME,"form-input.w-full.text-dark").click()
	elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='form-input w-full text-dark']")))
	elements[0].click()
	elements[0].send_keys("IT Army of Ukraine",)
	print (elements[0].get_attribute('placeholder'), "Type of elements[0]: ", type(elements[0]))
	# driver.execute_script("arguments[0].value = 'IT Army of Ukraine';", elements[0])

	time.sleep(4)
	# elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='form-input w-full text-dark']")))
	
	# time.sleep(5)
	table_trs = driver.find_elements(By.XPATH, '//table[@class="my-0 w-full"]')
	print(table_trs[0])
	df=0
	if table_trs is not None:
		print(table_trs[0].get_attribute('outerHTML'))
		df = pd.read_html(table_trs[0].get_attribute('outerHTML'))
		for k in df:
			print(k) 
	
	df.to_csv("Attacks.csv")
	print("Click done")

	while(True):
		pass	
launchBrowser()

