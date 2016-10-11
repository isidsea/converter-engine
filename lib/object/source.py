from .database        import Database
from .crawler         import Crawler
import pymongo

class Source:
	def __init__(self):
		conn = pymongo.MongoClient("mongodb://220.100.163.132/monitor")
		db   = conn["monitor"]
		
		self.crawlers = []
		for doc in db.crawlers_meta.find():
			crawler = Crawler(
				name = doc["name"],
				type = doc["type"],
				  db = Database(**doc["db"])
			)
			self.crawlers.append(crawler)