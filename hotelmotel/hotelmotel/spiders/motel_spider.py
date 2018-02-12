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
		self.driver = webdriver.Chrome(chrome_options=opts)
		#self.driver.set_window_size(1120, 550)
		#self.driver = webdriver.PhantomJS()
		
		
	def __del__(self):
		CrawlSpider.__del__(self)
		#self.driver.stop()
		#print(self.verificationErrors)
	
	#def start_requests(self):
		
		#url_pattern = "https://tripadvisor.com/{urlextension}"
		#file = open('urls.txt','r')
		#urls = file.read().split(',')
		#for url in urls:
		#	self.domains.append(url_pattern.format(urlextension=url[1:]))
		#yield scrapy.Request(url=self.domains[1], callback=self.parse)
		#for url in self.urls:
		#	yield scrapy.Request(url=url, callback=self.parse)
		
	def parse(self, response):
		self.driver.get('https://www.tripadvisor.com/Hotel_Review-g60625-d1863434-Reviews-Koloa_Landing_Resort_at_Poipu_Autograph_Collection-Poipu_Kauai_Hawaii.html')
		self.wait = WebDriverWait(self.driver, 500)
		print("launched website")
		items = []
		item = HotelmotelItem()
		site = self.driver.find_element_by_xpath(".//body")
		#self.driver.implicitly_wait(10)
		print("printing the data")

		elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//body/span/div[3]/div/div[1]")))
		elem = self.driver.find_element_by_xpath(".//h1[@id='HEADING']")
		elem.click()
		self.wait.until(EC.presence_of_element_located((By.XPATH, ".//body[@id='BODY_BLOCK_JQUERY_REFLOW']/span/div[4]")))
		element_ = self.driver.find_element_by_xpath(".//body[@id='BODY_BLOCK_JQUERY_REFLOW']/span/div[4]")
		elem.click()
		'''
		elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//body[@id='BODY_BLOCK_JQUERY_REFLOW']/span/div[4]")))
		elem = self.driver.find_element_by_xpath("//body[@id='BODY_BLOCK_JQUERY_REFLOW']/span/div[4]")
		elem.click()
		'''
		print("close date window")
		print(site.find_element_by_xpath(".//h1[@id='HEADING']").text) #hotel's name
		item['h_name'] = site.find_element_by_xpath(".//h1[@id='HEADING']").text #hotel's name
		#self.driver.execute_script("window.oldjQuery=window.jQuery;delete window.jQuery;delete window.$;window.oSend=XMLHttpRequest.prototype.send;XMLHttpRequest.prototype.send = function(){console.log('stopped ajax request', arguments)};")
		
		# Getting the number of reviews gave me some trouble due to dynamic website, so theres a few try loops here.  
		try:
			element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div/div[1]/div/span")
			if element_.is_displayed():
				print("found review number, method A!")
				item['h_reviewnums'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div/div[1]/div/span").text #review nums
		except:
			print("review number, method A failed, trying B")
			try:
				element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[1]/span[1]/div/a/span")
				if element_.is_displayed():
					print("found review number, method B!")
					item['h_reviewnums'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[1]/span[1]/div/a/span").text #review nums
			except:
				print("review number, method B failed, trying C")
				try:
					element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_resp_hr_atf_hotel_info_0']/div/div[1]/div/span")
					if element_.is_displayed():
						print("found review number, method C!")
						item['h_reviewnums'] = site.find_element_by_xpath(".//div[@id='taplc_resp_hr_atf_hotel_info_0']/div/div[1]/div/span").text #review nums
				except:
					print("giving up on this endeavor now")

		# Getting the hotel rank gave me some trouble, so theres a few try loops here.  
		try:
			element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[1]/span[2]/div/span/b")
			if element_.is_displayed():
				print("found review number, method A!")
				item['h_ranking'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[1]/span[2]/div/span/b").text
		except:
			print("review number, method A failed, trying B")		
			try:
				element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div/div[1]/div/span/b")
				if element_.is_displayed():
					print("found review number, method B!")
					item['h_ranking'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div/div[1]/div/span/b").text
			except:
				print("giving up on this endeavor now")
				
		
				
		# Address
		try:
			item['h_address1'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[2]/div/div[1]/span[2]").text #address 1
		except:
			self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@id='taplc_resp_hr_atf_hotel_info_0']/div/div[2]/div/div/div/div[1]/span[2]")))
			print("Waiting for address 1")
			item['h_address1'] = site.find_element_by_xpath(".//div[@id='taplc_resp_hr_atf_hotel_info_0']/div/div[2]/div/div/div/div[1]/span[2]").text #address 1
		
		try:
			item['h_address2'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[2]/div/div[1]/span[3]").text #address 2
		except:
			self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@id='taplc_resp_hr_atf_hotel_info_0']/div/div[2]/div/div/div/div[1]/span[3]")))
			print("Waiting for address 2")
			item['h_address2'] = site.find_element_by_xpath(".//div[@id='taplc_resp_hr_atf_hotel_info_0']/div/div[2]/div/div/div/div[1]/span[3]").text #address 2
		
		# Checkin dates
		try:
			element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_hr_atf_north_star_traveler_info_nostalgic_0']/div[2]/div[1]/span[1]/span/span[2]")
			print("found review number, method A!")
			item['checkin_dates'] = site.find_element_by_xpath(".//div[@id='taplc_hr_atf_north_star_traveler_info_nostalgic_0']/div[2]/div[1]/span[1]/span/span[2]").text
		except:
			print("checkin_dates, method A failed, trying B")	
			try:
				print("found checkin_dates, method B!")
				item['checkin_dates'] = site.find_element_by_xpath(".//div[@id='taplc_hr_atf_north_star_traveler_info_nostalgic_0']/div[2]/div[1]/span[1]/span/span[2]").text
			except:
				print("giving up on this endeavor now")
		
		try:
			item['checkout_dates'] = site.find_element_by_xpath(".//div[@id='taplc_hr_atf_north_star_traveler_info_nostalgic_0']/div[2]/div[1]/span[1]/span/span[2]").text
			print("Found checkout date, method A")
		except:
			item['checkout_dates'] = site.find_element_by_xpath(".//div[@id='taplc_trip_search_hr_responsive_0']/div/div[2]/div/span[3]/span[2]/span").text
			print("Found checkout date, method B")
		
		try:
			item['agency1_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[1]/span[2]").text #Agency 1 price
		except:
			try:
				item['agency1_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[1]/div[1]/div/div[2]").text #Agency 1 price
			except:
				self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[1]/div[1]/div/div")))
				item['agency1_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[1]/div[1]/div/div").text #Agency 1 price
		print("One is done!")
		try:
			item['agency1_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[1]/span[1]").text #Agency 1 name
		except:
			item['agency1_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[1]/span/img").text #Agency 1 name
		print("Two is done!")	
		try:
			item['agency2_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[2]/span[2]").text #Agency 2 price
		except:
			item['agency2_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div[1]/div/div[2]").text #Agency 2 name
		try:
			item['agency2_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[2]/span[1]").text #Agency 2 name
		except:
			item['agency2_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/span/img/").text #Agency 2 price	
			
		try:
			item['agency3_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[3]/span[2]").text #etc
		except:
			item['agency3_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[3]/div[1]/div/div[2]").text
		try:
			item['agency3_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[3]/span[1]").text
		except:
			item['agency3_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[3]/span/img/@alt").text #Agency 2 price
		
		try:
			item['agency4_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[4]/span[2]").text
		except:	
			item['agency4_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[4]/div/div[1]/span[2]/span[1]").text
		try:
			item['agency4_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[4]/span[1]").text
		except:
			item['agency4_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[4]/div/div[1]/span[1]").text
			
		print("Made it to 5")
		item['agency5_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[5]/span[2]").text
		item['agency5_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[5]/span[1]").text
		item['agency6_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[6]/span[2]").text
		item['agency6_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[6]/span[1]").text
		
		item['h_tripadvisor_rating'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[1]/span").text
		item['h_rating_excellent'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[1]/span[3]").text
		item['h_rating_vgood'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[2]/span[3]").text
		item['h_rating_avg'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[3]/span[3]").text
		item['h_rating_poor'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[4]/span[3]").text
		item['h_rating_terrible'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[5]/span[3]").text
		
		self.driver.execute_script("window.scrollTo(0, 500)") 
		item['h_amenities1'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[2]/div/div[2]/div[1]").text
		item['h_amenities2'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[2]/div/div[2]/div[2]").text
		item['h_amenities3'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[2]/div/div[2]/div[3]").text
		item['h_amenities4'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[2]/div/div[2]/div[4]").text
		item['h_amenities5'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[2]/div/div[2]/div[5]").text
		item['h_starrating'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[2]/div/div[2]/div[6]/div[2]").text
		item['h_rating_keyword1'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[4]/div[1]/a").text.encode("utf-8")
		item['h_rating_keyword2'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[4]/div[2]/a").text.encode("utf-8")
		item['h_rating_keyword3'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[4]/div[3]/a").text.encode("utf-8")
		elem = self.driver.find_element_by_xpath("//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[7]/div/span")
		elem.click()

		item['agency7_name'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[1]/span[1]").text
		item['agency7_price'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[1]/span[2]").text
		
		item['agency8_name'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[2]/span[1]").text
		item['agency8_price'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[2]/span[2]").text
		
		item['agency9_name'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[3]/span[1]").text
		item['agency9_price'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[3]/span[2]").text
		
		item['agency10_name'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[4]/span[1]").text
		item['agency10_price'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[4]/span[2]").text
		items.append(item)
		return items