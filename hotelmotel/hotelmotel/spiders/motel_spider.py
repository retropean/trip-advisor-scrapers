import scrapy
import datetime
import time as timer
from scrapy.spiders import Spider
from scrapy.selector import Selector
from datetime import date, time
from hotelmotel.items import HotelmotelItem

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.support import expected_conditions as EC
from scrapy.loader.processors import Join, MapCompose

import logging
from selenium.webdriver.remote.remote_connection import LOGGER


class MotelSpider(Spider):
	name = "hotelmotel"
	allowed_domains = ["tripadvisor.com"]
	domains = []
	start_urls = ["https://tripadvisor.com"]

	def __init__(self, daysoutcmmd=0, *args, **kwargs):
		LOGGER.setLevel(logging.WARNING)
		self.daysout = daysoutcmmd
		now = datetime.datetime.now() + datetime.timedelta(int(self.daysout))
		self.readyear = now.year
		self.readday = now.strftime('%d')
		self.readmonth = now.strftime('%m')
		#self.driver = webdriver.Firefox()
		opts = ChromeOptions()
		opts.add_experimental_option("detach", True)
		self.driver = webdriver.Chrome(chrome_options=opts, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
		self.driver.set_window_size(1024, 768)
		#self.driver = webdriver.PhantomJS()
		
		
	def __del__(self):
		CrawlSpider.__del__(self)
		#self.driver.stop()
		#print(self.verificationErrors)
	
	#def start_requests(self):
		
		#yield scrapy.Request(url=self.domains[1], callback=self.parse)
		#for url in self.urls:
		#	yield scrapy.Request(url=url, callback=self.parse)
		
	def parse(self, response):
		url_pattern = "https://tripadvisor.com/{urlextension}"
		file = open('urls.txt','r')
		urls = file.read().split(',')
		for url in urls:
			self.domains.append(url_pattern.format(urlextension=url[1:]))
		print(self.domains)
		for domainz in self.domains:
			self.driver.get(domainz)
			self.wait = WebDriverWait(self.driver, 500)
			i=0
			filename = domainz.split(".com/",1)[1] 
			print("launched website")
			items = []
			item = HotelmotelItem()
			site = self.driver.find_element_by_xpath(".//body")
			print("site is here")
			
			thesource= (self.driver.page_source).encode("utf-8")
			file_ = open(filename+'.html', 'wb')
			file_.write(thesource)
			file_.close()
			
			elem = self.driver.find_element_by_xpath(".//h1[@id='HEADING']")
			elem.click()
			
			self.driver.execute_script("window.scrollTo(0, 3000)") 
			elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='prw_rup prw_common_responsive_pagination mobile-more']/div/span[2]")))
			elem = self.driver.find_element_by_xpath("//div[@class='prw_rup prw_common_responsive_pagination mobile-more']/div/span[2]")
			elem.click()
			while(i<5):
				timer.sleep(10)
				thesource= (self.driver.page_source).encode("utf-8")
				thefilename = filename + str(i)
				file_ = open(thefilename+'.html', 'wb')
				file_.write(thesource)
				file_.close()
				
				self.driver.execute_script("window.scrollTo(0, 1200)") 
				elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='prw_rup prw_common_responsive_pagination mobile-more']/div/span[2]")))
				elem = self.driver.find_element_by_xpath("//div[@class='prw_rup prw_common_responsive_pagination mobile-more']/div/span[2]")
				elem.click()
				i = i+1