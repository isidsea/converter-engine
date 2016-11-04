from . import Logger
import arrow

class ConverterLogger(Logger):

	def __init__(self):
		Logger.__init__(self)

	def log(self, level=None, state=None, message=None, number_of_documents=None, **kwargs):
		assert level is not None, "level is not defined."
		assert state is not None, "state is not defined."

		document = {
			       		  "level" : level,
			       		  "state" : state,
			"number_of_documents" : number_of_documents
				   "_insert_time" : arrow.utcnow().datetime,
			         		"TTL" : arrow.utcnow().datetime
		}
		if message is not None:
			document.update({"message":message})

		for key,value in kwargs.items():
			document.update({"_%s" % key: value})
		self.logs.append(document)