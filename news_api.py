#!/usr/bin/env python3

import requests
import api_key


raw_url = "https://newsapi.org/v2/top-headlines?sources="
and_url = "&"
spiegel_url = "spiegel-online"
api_url = "apiKey={0}".format(api_key.news_api_key)
url = raw_url + spiegel_url + and_url + api_url
resp = requests.get(url)
headlines = resp.json()
print(headlines.keys())
print(headlines["status"])
print(headlines["totalResults"])
for i in headlines["articles"]:
	print(i["title"])
