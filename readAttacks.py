from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from bs4 import BeautifulSoup as bs
import re, os, time

PATH = "C:\Program Files (x86)\chromedriver.exe"
link = "https://cyberconflicts.cyberpeaceinstitute.org/threats/attack-details"
driver = ""

def getCountry(tdCountry):
	countryPattern = r'data-original-title="([\w\s]+)"'
	matches = re.search(countryPattern, tdCountry)
	return (matches.group(1) if matches else "No match found")

def getCertainty(tdCertainty):
	certaintyPattern = r'data-original-title="([^"]+)"'
	matches = re.search(certaintyPattern, tdCertainty)
	return (matches.group(1) if matches else "No match found")

def saveDFToStorage(df, searchFor):
	if not  os.path.exists("output"):
		# Create a new directory
		os.makedirs("output")
	output_path="output/Attacks_{}.csv".format(searchFor)
	#Append if exists
	df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))
	print("\nSave Successful!\n")

def launchBrowser(noOfPages, searchFor):
	chrome_options = Options()
	chrome_options.add_argument("disable-infobars");
	driver = webdriver.Chrome(executable_path=PATH, chrome_options=chrome_options)	
	driver.get(link)

	#Comment below three lines to search for the whole website
	# elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='form-input w-full text-dark']")))
	# elements[0].click()
	# elements[0].send_keys(searchFor,)

	time.sleep(2)

	while noOfPages != 0:
		# time.sleep(6)

		df=0
		table_trs = driver.find_elements(By.XPATH, '//table[@class="my-0 w-full"]')

		if table_trs is not None:
			#Select the first table if multiple are found
			tableOuterHTML = table_trs[0].get_attribute('outerHTML')

			df = pd.read_html(tableOuterHTML)[0]
			
			table = bs(tableOuterHTML, "html.parser")
			countryNames = []
			certainty = []

			rows = table.find_all("tr")
			# Leaving Header, slice[1:]
			for row in rows[1:]:
				trs = row.find_all("td")
				print("Country Code: ", getCountry(str(trs[1])))
				print("TR: ", trs[1])
				countryNames.append(getCountry(str(trs[1])))
				certainty.append(getCertainty(str(trs[7])))

			df['Country'] = countryNames
			df['Certainty'] = certainty

			saveDFToStorage(df, searchFor)

		#Click for the next page
		element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".svg-inline--fa.fa-angle-right")))
		element.click()
		noOfPages-=1
		time.sleep(0.3)

	print("Done!!")

	while(True):
		pass	


noOfPages = 133 #Attention!
searchFor = "ALL"
launchBrowser(noOfPages, searchFor)

