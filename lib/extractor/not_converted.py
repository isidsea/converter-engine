from ..exceptions import CannotFindDocument
import pymongo
import re

class NotConvertedExtractor:
	def __init__(self):
		pass

	def extract(self, crawler=None):
		""" Exceptions:
			- AssertionError
			- CannotFindDocument
		"""
		assert crawler is not None, "database is not defined."
		
		conn = pymongo.MongoClient("mongodb://%s/%s" % (
			crawler.db.host,
			crawler.db.name
		))
		db   = conn[crawler.db.name]

		try:
			doc = db[crawler.db.collection].find_one({"converted":False})
			if "_crawled_by" in doc:
				docs = db[crawler.db.collection].find({
					"$and":[
						{"converted":False},
						{"_crawled_by": re.compile(crawler.name, re.IGNORECASE)}
					]
				})
			else:
				docs = db[crawler.db.collection].find({"converted": False})
		except TypeError as ex:
			raise CannotFindDocument("%s not converted is 0" % crawler.name)
		finally:
			conn.close()
		return docs