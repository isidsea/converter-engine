from ..logger import Logger
import pymongo

class LogSaver:
	def __init__(self):
		pass

	def save(self, logger=None):
		assert logger                    is not None, "logger is not defined."
		assert type(logger).__bases__[0] is Logger  , "incorrect logger data type."

		conn = pymongo.MongoClient("mongodb://220.100.163.132/monitor")
		db   = conn["monitor"]

		db.converter.create_index("level", background=True)
		db.converter.create_index("state", background=True)
		db.converter.create_index("TTL", expireAfterSeconds=60*60*24*15)

		for log in logger.logs:
			db.converter.insert_one(log)
		logger.saved_logs.extend(logger.logs)
		logger.logs.clear()
		conn.close()
