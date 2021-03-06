from .database        import Database
from .crawler         import Crawler
import pymongo

class Source:
	def __init__(self):
		conn = pymongo.MongoClient("mongodb://mongo:27017/monitor")
		db   = conn["monitor"]
		
		self.crawlers = []
		for doc in db.crawlers_meta.find():
			crawler = Crawler(
				name = doc["name"],
				type = doc["type"],
				  db = Database(**doc["db"])
			)
			self.crawlers.append(crawler)
		conn.close()