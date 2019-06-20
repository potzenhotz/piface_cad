#!/usr/bin/env python3

import requests
import api_key

class news_api:
	def __init__(self, source):
		self.url = self.set_url(api_key.news_api_key, source)
		self.news = self.get_news()

	def set_url(self, news_api_key, source):
		raw_url = "https://newsapi.org/v2/top-headlines?sources="
		and_url = "&"
		source_url = source
		api_url = "apiKey={0}".format(news_api_key)
		return raw_url + source_url + and_url + api_url

	def get_news(self):
		resp = requests.get(self.url)
		return resp.json()

	def update_news(self):
		self.news = self.get_news()

	def replace_non_breaking_space(self, string):
		return string.replace(u'\xa0', u' ')

	def replace_umlaute(self, string):
		umlaute = {'ö':'oe','ä':'ae','ü':'ue', 'Ö': 'Oe', 'Ü':'Ue', 'Ä':'Ae'}
		for umlaut in umlaute:
		    string = string.replace(umlaut,umlaute[umlaut])

class spiegel_news(news_api):
	def __init__(self):
		super().__init__("spiegel-online")
		self.headlines = self.get_headlines()
	
	def get_headlines(self):
		headlines = []
		for article in self.news["articles"]:
			headline = self.replace_non_breaking_space(article["title"])
			headline = self.replace_umlaute(headline)
			headlines.append(headline)
		return headlines
	


if __name__=="__main__":
	spiegel = spiegel_news()
	#print(spiegel.get_news())
	print(spiegel.get_headlines())
	
