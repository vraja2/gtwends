import pycurl
import cStringIO
import re 
import tweepy 

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

consumer_key= "wPS9eunNZY2x49O16bZcg"
consumer_secret = "7rR7ckljLpwxoNPCrVf174SNZL7IXE4rhTUxLqNpY"

access_token = "15640755-d9nI62E67Pr4UyNOdwfvNqsTsOBGLM9wkgrE6t5mH"
access_token_secret = "8OYioeKAXoAd4rfVfsowEvxWjbCXu1SgHra2AruqE"


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
