import pycurl
import cStringIO
import re 
import tweepy 
import configuration 
import json
import requests
from colorama import Fore, Back, Style

class GoogleHotTrends:
	
	def fetch_trends(self):
		trendsURL = 'http://www.google.com/trends/hottrends/atom/hourly'
		buf = cStringIO.StringIO()
		c = pycurl.Curl()
		c.setopt(pycurl.URL, trendsURL)
		c.setopt(c.WRITEFUNCTION, buf.write)
		c.perform()
		responsedata = buf.getvalue()
		buf.close()
		return self.parse_trend(responsedata)
	
	def parse_trend(self, response):
		subjects = re.findall('.+?<a href=".+?">(.+?)<\/a>.+?', str(response))
		return subjects
				
	
trends = GoogleHotTrends()
keywords = trends.fetch_trends()
print keywords

# configuration file not included on github. make a configuration.py file.

consumer_key= configuration.consumer_key
consumer_secret = configuration.consumer_secret

access_token = configuration.access_token
access_token_secret = configuration.access_token_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

jsonURL= 'http://www.sentiment140.com/api/bulkClassifyJson'


api = tweepy.API(auth)
print api.me().name
for y in xrange(0,len(keywords)):
	total = 0
	print("------------------------------")
	print Fore.WHITE + keywords[y]    #iterate through trend topics
	result = api.search(keywords[y])
	counter = 0
	for x in xrange(0,len(result)):   #iterate through trend related tweets
		d = {'data': [{'text': result[x].text}]}
		r = requests.post(jsonURL, data = json.dumps(d))
		jsonContent = json.loads(r.text)
		polVal = jsonContent["data"][0]["polarity"]
		if polVal == 0:
			print Fore.RED + result[x].text
			total+=polVal
			counter+=1
		elif polVal == 4:
			print Fore.GREEN + result[x].text
			total+=polVal
			counter+=1
		elif polVal == 2:
			print Fore.WHITE + result[x].text
	if counter != 0:
		print Fore.WHITE + str(total/counter)
	else:
		print Fore.WHITE + str(2)
