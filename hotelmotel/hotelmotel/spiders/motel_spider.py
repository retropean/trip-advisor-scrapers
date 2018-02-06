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
from selenium.webdriver.support import expected_conditions as EC
from scrapy.loader.processors import Join, MapCompose

import logging
from selenium.webdriver.remote.remote_connection import LOGGER


class MotelSpider(Spider):
	name = "hotelmotel"
	allowed_domains = ["https://tripadvisor.com"]
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
		self.driver = webdriver.Chrome()
		#self.driver.set_window_size(1120, 550)
		#self.driver = webdriver.PhantomJS()
		
		
	def __del__(self):
		self.selenium.stop()
		print self.verificationErrors
		CrawlSpider.__del__(self)
	
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
		self.wait = WebDriverWait(self.driver, 20)
		print 'hello'
		items = []
		item = HotelmotelItem()
		site = self.driver.find_element_by_xpath(".//body")
		#self.driver.implicitly_wait(10)
		print 'printing the data'

		elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//body/span/div[3]/div/div[1]")))
		elem = self.driver.find_element_by_xpath(".//h1[@id='HEADING']")
		elem.click()
		'''
		elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//body[@id='BODY_BLOCK_JQUERY_REFLOW']/span/div[4]")))
		elem = self.driver.find_element_by_xpath("//body[@id='BODY_BLOCK_JQUERY_REFLOW']/span/div[4]")
		elem.click()
		'''
		print 'closing annoying date window'
		#self.driver.implicitly_wait(10)
		print site.find_element_by_xpath(".//h1[@id='HEADING']").text #hotel's name
		item['h_name'] = site.find_element_by_xpath(".//h1[@id='HEADING']").text #hotel's name
		self.driver.execute_script("window.oldjQuery=window.jQuery;delete window.jQuery;delete window.$;window.oSend=XMLHttpRequest.prototype.send;XMLHttpRequest.prototype.send = function(){console.log('stopped ajax request', arguments)};")
		
		#self.driver.find_element_by_xpath(".//div[@id='taplc_resp_hr_atf_hotel_info_0']/div/div[1]/div/span").is_displayed()
		#if(EC.presence_of_element_located((By.XPATH, ".//div[@id='taplc_resp_hr_atf_hotel_info_0']/div/div[1]/div/span")) == True):
		try:
			element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div/div[1]/div/span")
			if element_.is_displayed():
				print "found a!"
				print site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div/div[1]/div/span").text #review nums
				item['h_reviewnums'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div/div[1]/div/span").text #review nums
		except:
			print 'fuck'
			try:
				element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[1]/span[1]/div/a/span")
				if element_.is_displayed():
					print "found b!"
					print site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[1]/span[1]/div/a/span").text #review nums
			except:
				print 'fuck'
				try:
					element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_resp_hr_atf_hotel_info_0']/div/div[1]/div/span")
					if element_.is_displayed():
						print "found c!"
						print site.find_element_by_xpath(".//div[@id='taplc_resp_hr_atf_hotel_info_0']/div/div[1]/div/span").text #review nums
				except:
					print 'fuck'

		try:
			element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[1]/span[2]/div/span/b")
			if element_.is_displayed():
				print "found a!"
				print site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[1]/span[2]/div/span/b").text #rank
				item['h_ranking'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[1]/span[2]/div/span/b").text #review nums
		except:
			print 'fuck'		
			try:
				element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div/div[1]/div/span/b")
				if element_.is_displayed():
					print "found b!"
					print site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div/div[1]/div/span/b").text #rank 
					item['h_ranking'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div/div[1]/div/span/b").text #review nums
			except:
				print 'fuck'
		#print site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div/div[1]/div/span").text #ranking
		#print site.find_element_by_xpath(".//div[@id='taplc_resp_hr_atf_hotel_info_0']/div/div[1]/div/div/span/b").text #ranking
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[2]/div/div[1]/span[2]").text #address 1
		item['h_address1'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[2]/div/div[1]/span[2]").text #review nums
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[2]/div/div[1]/span[3]").text #address 2
		item['h_address2'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_header_hotels_0']/div[2]/div/div[1]/span[3]").text #review nums
		try:
			element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_hr_atf_north_star_traveler_info_nostalgic_0']/div[2]/div[1]/span[1]/span/span[2]")
			if element_.is_displayed():
				print "found a!"
				print site.find_element_by_xpath(".//div[@id='taplc_hr_atf_north_star_traveler_info_nostalgic_0']/div[2]/div[1]/span[1]/span/span[2]").text #checkin
				item['checkin_dates'] = site.find_element_by_xpath(".//div[@id='taplc_hr_atf_north_star_traveler_info_nostalgic_0']/div[2]/div[1]/span[1]/span/span[2]").text
		except:
			print 'fuck'
		try:
			element_ = self.driver.find_element_by_xpath(".//div[@id='taplc_trip_search_hr_responsive_0']/div/div[2]/div/span[1]/span[2]/span")
			if element_.is_displayed():
				print "found b!"
				print site.find_element_by_xpath(".//div[@id='taplc_trip_search_hr_responsive_0']/div/div[2]/div/span[1]/span[2]/span").text #checkin
				item['checkin_dates'] = site.find_element_by_xpath(".//div[@id='taplc_hr_atf_north_star_traveler_info_nostalgic_0']/div[2]/div[1]/span[1]/span/span[2]").text
		except:
			print 'fuck'
		
		print site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[1]/span[2]").text #price
		print site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[1]/span[1]").text
		item['agency1_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[1]/span[2]").text
		item['agency1_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[1]/span[1]").text
		
		print site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[2]/span[2]").text
		print site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[2]/span[1]").text
		item['agency2_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[2]/span[2]").text
		item['agency2_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[2]/span[1]").text
		
		print site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[3]/span[2]").text #price
		print site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[3]/span[1]").text
		item['agency3_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[3]/span[2]").text
		item['agency3_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[3]/span[1]").text
		
		print site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[4]/span[2]").text
		print site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[4]/span[1]").text
		item['agency4_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[4]/span[2]").text
		item['agency4_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[4]/span[1]").text
		
		print site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[5]/span[2]").text
		print site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[5]/span[1]").text
		item['agency5_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[5]/span[2]").text
		item['agency5_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[5]/span[1]").text
		
		print site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[6]/span[2]").text
		print site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[6]/span[1]").text
		item['agency6_price'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[6]/span[2]").text
		item['agency6_name'] = site.find_element_by_xpath(".//div[@id='taplc_hr_north_star_v1_meta_0']/div[2]/div[2]/div/div[2]/div/div[6]/span[1]").text
		
		print site.find_element_by_xpath(".//div[@id='taplc_hr_atf_north_star_traveler_info_nostalgic_0']/div[2]/div[1]/span[2]/span/span[2]").text #checkout
		item['checkout_dates'] = site.find_element_by_xpath(".//div[@id='taplc_hr_atf_north_star_traveler_info_nostalgic_0']/div[2]/div[1]/span[1]/span/span[2]").text
		
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[1]/span").text #rating
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[1]/span[3]").text #rating
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[2]/span[3]").text #rating
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[3]/span[3]").text #rating
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[4]/span[3]").text #rating
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[5]/span[3]").text #rating
		item['h_tripadvisor_rating'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[1]/span").text
		item['h_rating_excellent'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[1]/span[3]").text
		item['h_rating_vgood'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[2]/span[3]").text
		item['h_rating_avg'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[3]/span[3]").text
		item['h_rating_poor'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[4]/span[3]").text
		item['h_rating_terrible'] = site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[2]/ul/li[5]/span[3]").text
		
		self.driver.execute_script("window.scrollTo(0, 500)") 
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[2]/div/div[2]/div[1]").text #amenities
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[2]/div/div[2]/div[2]").text #amenities
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[2]/div/div[2]/div[3]").text #amenities
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[2]/div/div[2]/div[4]").text #amenities
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[2]/div/div[2]/div[5]").text #amenities
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[2]/div/div[2]/div[6]/div[2]").text #hotelrating
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[4]/div[1]/a").text.encode("utf-8") #keyword1
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[4]/div[2]/a").text.encode("utf-8") #keyword2
		print site.find_element_by_xpath(".//div[@id='taplc_location_detail_overview_hotel_map_pins_default_0']/div/div[2]/div[2]/div[1]/div[4]/div[3]/a").text.encode("utf-8") #keyword3
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
		
		print site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[1]/span[1]").text #price
		print site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[1]/span[2]").text #price
		item['agency7_name'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[1]/span[1]").text
		item['agency7_price'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[1]/span[2]").text
		
		print site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[2]/span[1]").text #price
		print site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[2]/span[2]").text #price
		item['agency8_name'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[2]/span[1]").text
		item['agency8_price'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[2]/span[2]").text
		
		print site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[3]/span[1]").text #price
		print site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[3]/span[2]").text #price
		item['agency9_name'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[3]/span[1]").text
		item['agency9_price'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[3]/span[2]").text
		
		print site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[4]/span[1]").text #price
		print site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[4]/span[2]").text #price
		item['agency10_name'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[4]/span[1]").text
		item['agency10_price'] = site.find_element_by_xpath(".//div[@class='prw_rup prw_common_base_dropdown ui_options']/div/div[4]/span[2]").text
		items.append(item)
		return items
		'''
		sel = Selector(response)
		items = []
		item = HotelmotelItem()
		site = sel.xpath('.//div[@id="PAGE"]')
		#for site in sites:
		item['h_name'] = site.xpath('.//h1[@id="HEADING"]/text()').extract() #hotel's name
		item['h_reviewnums'] = site.xpath('.//div[@id="taplc_location_detail_header_hotels_0"]/div[1]/span[1]/div/a/span/text()').extract()
		item['h_ranking'] = site.xpath('.//div[@id="taplc_location_detail_header_hotels_0"]/div[1]/span[2]/div/span/b/text()').extract()
		item['h_address1'] = site.xpath('.//div[@id="taplc_location_detail_header_hotels_0"]/div[2]/div/div[1]/span[2]/text()').extract()
		item['h_address2'] = site.xpath('.//div[@id="taplc_location_detail_header_hotels_0"]/div[2]/div/div[1]/span[3]/text()').extract()
		item['h_phone'] = site.xpath('.//div[@id="taplc_location_detail_header_hotels_0"]/div[2]/div/div[2]/span[2]/text()').extract()
		print 'here it is'
		print site.xpath('.//div[@id="taplc_location_detail_overview_hotel_map_pins_default_0"]/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/text()').extract()
		print site.xpath('.//div[@id="taplc_location_detail_overview_hotel_map_pins_default_0"]/div/div[2]/div[2]/div[2]/div/div[2]/div[8]/div[2]/text()').extract()
		
		item['checkin_dates'] = (response.request.url[-6:])[:4]
		item['checkout_dates'] = (response.request.url[-6:])[:4]
		item['agency1_price'] = (response.request.url[-6:])[:4]
		item['agency2_price'] = (response.request.url[-6:])[:4]
		item['agency3_price'] = (response.request.url[-6:])[:4]
		item['agency4_price'] = (response.request.url[-6:])[:4]
		item['agency5_price'] = (response.request.url[-6:])[:4]
		item['agency6_price'] = (response.request.url[-6:])[:4]
		item['agency1_name'] = (response.request.url[-6:])[:4]
		item['agency2_name'] = (response.request.url[-6:])[:4]
		item['agency3_name'] = (response.request.url[-6:])[:4]
		item['agency4_name'] = (response.request.url[-6:])[:4]
		item['agency5_name'] = (response.request.url[-6:])[:4]
		item['agency6_name'] = (response.request.url[-6:])[:4]
		item['h_amenities1'] = (response.request.url[-6:])[:4]
		item['h_amenities2'] = (response.request.url[-6:])[:4]
		item['h_amenities3'] = (response.request.url[-6:])[:4]
		item['h_amenities4'] = (response.request.url[-6:])[:4]
		item['h_amenities5'] = (response.request.url[-6:])[:4]
		item['h_amenities6'] = (response.request.url[-6:])[:4]
		item['h_amenities7'] = (response.request.url[-6:])[:4]
		item['h_starrating'] = (response.request.url[-6:])[:4]
		item['h_tripadvisor_rating'] = (response.request.url[-6:])[:4]
		item['h_rating_excellent'] = (response.request.url[-6:])[:4]
		item['h_rating_vgood'] = (response.request.url[-6:])[:4]
		item['h_rating_avg'] = (response.request.url[-6:])[:4]
		item['h_rating_poor'] = (response.request.url[-6:])[:4]
		item['h_rating_terrible'] = (response.request.url[-6:])[:4]
		item['h_rating_keyword1'] = (response.request.url[-6:])[:4]
		item['h_rating_keyword2'] = (response.request.url[-6:])[:4]
		item['h_rating_keyword3'] = (response.request.url[-6:])[:4]
		'''