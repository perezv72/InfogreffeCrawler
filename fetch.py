#!/usr/bin/env python2
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import os.path

browser = webdriver.Chrome()
time.sleep(3)
# the script needs a list of SIRET numbers formatted in the manner shown below
siret = ['409 546 389','421 000 472','401 318 621','420 796 591','421 002 866','499 665 537','500 993 969','500 994 199','501 137 483','511 376 600']

for item in siret:
	browser.get('https://www.infogreffe.fr/societes/recherche-siret-entreprise/chercher-siret-entreprise.html')
	browser.find_element_by_id('p1_siren').send_keys(item)
	time.sleep(10)
	browser.find_element_by_id('boutonRechercherEntreprise_label').click()
	time.sleep(5)
	n = len([name for name in os.listdir('.') if os.path.isfile(name)])
	n2 = n + 1
	n3 = "%02d"%n2
	html = browser.page_source
	html_file = open(str(n3) +".html", "w")
	html_file.write(html)
	html_file.close()
	print("fetch siret # " + str(item) + "; html file name: " +str(n2))
