import os
import sys

TEST_DIR   = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)

from lib.factory.logger import LoggerFactory
from lib.factory.saver  import SaverFactory
import pymongo
import pytest

class TestConverterLog:
	@classmethod
	def setup_class(cls):
		cls.conn = pymongo.MongoClient("mongodb://220.100.163.132/monitor")
		cls.db   = cls.conn["monitor"]

	@classmethod
	def teardown_class(cls):
		cls.db.converter.remove({"_test":True})
		cls.conn.close()

	@pytest.fixture
	def result_log(self):
		return {
			  "level" : 0,
			  "state" : "START",
			  "_test" : True,
			"message" : "Converting Kaskus Crawler"
		}

	@pytest.fixture
	def sample_log(self):
		logger = LoggerFactory.get_logger(LoggerFactory.CONVERTER)
		logger.log(
			  level = logger.DEBUG, 
			  state = "START", 
			message = "Converting Kaskus Crawler", 
			   test = True
		)
		return logger

	def test_log(self, sample_log, result_log):
		log = sample_log.logs[0]
		del log["_insert_time"]

		assert log == result_log

	def test_save_log(self, sample_log, result_log):
		saver = SaverFactory.get_saver(SaverFactory.LOG)
		saver.save(sample_log)

		documents = self.db.converter.find({},).sort("_insert_time", -1).limit(1)
		for document in documents:
			assert "_insert_time" in document
			del document["_insert_time"]
			del document["_id"]
			assert document == result_log
