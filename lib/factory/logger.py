from ..logger.converter import ConverterLogger

class LoggerFactory:
	CONVERTER = 0

	def __init__(self):
		pass

	@classmethod
	def get_logger(self, logger_name=None):
		assert logger_name is not None, "logger_name is not defined."

		if logger_name == LoggerFactory.CONVERTER:
			return ConverterLogger()