import pycurl
import cStringIO
import re 
import tweepy 
import configuration 

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


api = tweepy.API(auth)
print api.me().name
for y in xrange(0,len(keywords)):
	print("------------------------------")
	print keywords[y]
	result = api.search(keywords[y])
	for x in xrange(0,len(result)):
		print result[x].text
