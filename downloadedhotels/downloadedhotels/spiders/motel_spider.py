import scrapy
import datetime
import time as timer
import os
from scrapy.spiders import Spider
from scrapy.selector import Selector
from datetime import date, time
from downloadedhotels.items import DownloadedhotelsItem


class MotelSpider(Spider):
	name = "motelspider"
	filelist = os.listdir("C:/Users/00811289/Documents/github/trip-advisor-scrapers/downloadedhotels/hotel_html")
	
	
	def start_requests(self):
		for file in self.filelist:
			yield scrapy.Request(url="file:///C:/Users/00811289/Documents/github/trip-advisor-scrapers/downloadedhotels/hotel_html/"+file, callback=self.parse)

	def parse(self, response):
		print("loading new file")
		sel = Selector(response)
		items = []
		item = DownloadedhotelsItem()
		site =  sel.xpath(".//body")
		item['h_name'] = site.xpath('.//h1[@id="HEADING"]/text()').extract() # hotel name
		item['h_reviewnums'] = site.xpath('.//div[@id="taplc_resp_hr_atf_hotel_info_0"]/div/div[1]/div/span/text()').extract() # review numbers
		item['h_ranking'] = site.xpath('.//div[@id="taplc_resp_hr_atf_hotel_info_0"]/div/div[1]/div/div/span/b/text()').extract() # rank
		item['h_address1'] = site.xpath('.//div[@id="taplc_resp_hr_atf_hotel_info_0"]/div/div[2]/div/div/div/div[1]/span[2]/text()').extract() # address 1
		item['h_address2'] = site.xpath('.//div[@id="taplc_resp_hr_atf_hotel_info_0"]/div/div[2]/div/div/div/div[1]/span[3]/text()').extract() # address 2
		item['h_phone'] = site.xpath('.//div[@id="taplc_resp_hr_atf_hotel_info_0"]/div/div[2]/div/div/div/div[2]/a/span[2]/text()').extract() # phone
		item['checkin_dates'] = site.xpath('.//div[@id="taplc_trip_search_hr_responsive_0"]/div/div[2]/div/span[1]/span[2]/span/text()').extract() # checkin
		item['checkout_dates'] = site.xpath('.//div[@id="taplc_trip_search_hr_responsive_0"]/div/div[2]/div/span[3]/span[2]/span/text()').extract() # checkout
		item['h_amenities1'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[1]/text()').extract()
		item['h_amenities2'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/text()').extract()
		item['h_amenities3'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[3]/text()').extract()
		item['h_amenities4'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[4]/text()').extract()
		item['h_amenities5'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div[5]/text()').extract()
		item['h_amenities6'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/text()').extract()
		item['h_amenities7'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/text()').extract()
		item['h_starrating'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[3]/text()').extract()
		item['h_tripadvisor_rating'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[1]/div[1]/span/text()').extract()
		item['h_rating_excellent'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[1]/div[2]/ul/li[1]/span[3]/text()').extract()
		item['h_rating_vgood'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[1]/div[2]/ul/li[2]/span[3]/text()').extract()
		item['h_rating_avg'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[1]/div[2]/ul/li[3]/span[3]/text()').extract()
		item['h_rating_poor'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[1]/div[2]/ul/li[4]/span[3]/text()').extract()
		item['h_rating_terrible'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[1]/div[2]/ul/li[5]/span[3]/text()').extract()
		item['h_rating_terrible'] = site.xpath('.//div[@id="taplc_hotel_detail_overview_responsive_0"]/div/div[2]/div/div[1]/div[2]/ul/li[5]/span[3]/text()').extract()
		item['h_review1'] = site.xpath('//div[@id="taplc_location_reviews_list_resp_hr_resp_0"]/div/div[3]/div[2]/div/div/div/div/div[2]/div/p/text()').extract()
		item['h_review2'] = site.xpath('//div[@id="taplc_location_reviews_list_resp_hr_resp_0"]/div/div[4]/div[3]/div/div/div/div[2]/div[2]/div/p/text()').extract()
		item['h_review3'] = site.xpath('//div[@id="taplc_location_reviews_list_resp_hr_resp_0"]/div/div[5]/div[3]/div/div/div/div[2]/div[2]/div/p/text()').extract()
		item['h_review4'] = site.xpath('//div[@id="taplc_location_reviews_list_resp_hr_resp_0"]/div/div[6]/div[3]/div/div/div/div[2]/div[2]/div/p/text()').extract()
		item['h_review5'] = site.xpath('//div[@id="taplc_location_reviews_list_resp_hr_resp_0"]/div/div[7]/div[3]/div/div/div/div[2]/div[2]/div/p/text()').extract()
		items.append(item)
		return items