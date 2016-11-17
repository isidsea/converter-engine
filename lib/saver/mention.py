from lib.exceptions import DuplicateMention, NetworkTimeout
import pymongo
import re
import arrow

class MentionSaver:
	def __init__(self):
		pass

	def save(self, mention=None):
		""" Exception:
			- AssertionError
			- DuplicateMention
			- NetworkTimeout
		"""
		assert mention is not None, "mention is not defined."

		conn = pymongo.MongoClient("mongodb://alex:07081984@220.100.163.138/?authSource=admin")
		db   = conn["isid"]

		try:
			db.mention.insert_one(mention.to_dict())
		except pymongo.errors.DuplicateKeyError:
			raise DuplicateMention("Ops! Duplicate Mention!")
		except pymongo.errors.NetworkTimeout:
			raise NetworkTimeout("Network Timeout!")
		except pymongo.errors.AutoReconnect:
			raise NetworkTimeout("Auto Reconnect!")
		except pymongo.errors.ServerSelectionTimeoutError:
			raise NetworkTimeout("Server Selection Timeout!")
		finally:
			conn.close()	

	def set_as_converted(self, crawler=None, mention=None):
		""" Exceptions:
			- AssertionError
			- NetworkTimeout
		"""
		assert crawler is not None, "crawler is not defined."
		assert mention is not None, "mention is not defined."

		# Update status of last converted time for certain crawler
		conn = pymongo.MongoClient("mongodb://mongo:27017/monitor")
		db   = conn["monitor"]
		db.status.update(
			{"crawler_name": re.compile(crawler.name, re.IGNORECASE)}, 
			{"$set":{"last_converted_time": arrow.utcnow().datetime}},
			upsert = True
		)
		conn.close()

		conn = pymongo.MongoClient("mongodb://%s:%s/%s" % (
			crawler.db.host,
			crawler.db.port,
			crawler.db.name
		))
		db = conn[crawler.db.name]
		
		try:
			db[crawler.db.collection].update(
				{"permalink":mention.MentionDirectLink},
				{"$set":{"converted":True}}
			)
		except pymongo.errors.NetworkTimeout:
			raise NetworkTimeout("Network Timeout!")
		except pymongo.errors.AutoReconnect:
			raise NetworkTimeout("Auto Reconnect!")
		except pymongo.errors.ServerSelectionTimeoutError:
			raise NetworkTimeout("Server Selection Timeout!")
		finally:
			conn.close()