from ..extractor.not_converted import NotConvertedExtractor

class ExtractorFactory:
	NOT_CONVERTED = 0

	def __init__(self):
		pass

	@classmethod
	def get_extractor(self, extractor_name=None):
		assert extractor_name is not None, "extractor_name is not defined."

		if extractor_name == ExtractorFactory.NOT_CONVERTED:
			return NotConvertedExtractor()