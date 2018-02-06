import scrapy
import datetime
import time
from scrapy.spiders import Spider
from scrapy.selector import Selector
from datetime import date, time
from ericstrip.items import EricstripItem

class MBSpider(Spider):
	custom_settings = {
		"DOWNLOAD_DELAY": 5.0,
		"RETRY_ENABLED": True,
	}
	name = "ericstrip"
	allowed_domains = ["tripadvisor.com"]
	urls = []

	def __init__(self, daysoutcmmd=0, *args, **kwargs):
		self.daysout = daysoutcmmd
		now = datetime.datetime.now() + datetime.timedelta(int(self.daysout))
		self.readyear = now.year
		self.readday = now.day
		self.readmonth = now.month
	
	def start_requests(self):
		yield scrapy.Request(url="https://www.tripadvisor.com/Hotels-g29218-Kauai_Hawaii-Hotels.html", callback=self.parse)

	def parse(self, response):
		sel = Selector(response)
		
		site = sel.xpath('.//div[@class="ppr_rup ppr_priv_hsx_hotel_list_lite"]')
		
		item = EricstripItem()
		items = []
		i = 0
		
		totallist = site.xpath('.//div/div/div[1]/@data-url').extract()
		print totallist
		f = open('urls.txt','w')
		
		while i < len(totallist):
			f.write(totallist[i])
			f.write(",")
			#print items
			i = i + 1
		return items