import pymongo

class NotConvertedExtractor:
	def __init__(self):
		pass

	def extract(self, crawler=None):
		assert crawler is not None, "database is not defined."

		conn = pymongo.MongoClient("mongodb://%s/%s" % (
			crawler.db.host,
			crawler.db.name
		))
		db   = conn[crawler.db.name]
		docs = db[crawler.db.collection].find({"converted":False})
		conn.close()
		return docs