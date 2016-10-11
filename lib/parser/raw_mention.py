from ..template.mention import MentionTemplate
import bson.json_util

class RawMentionParser:
	def __init__(self):
		pass

	def parse(self, crawler=None, raw=None):
		assert raw     is not None, "raw is not defined."
		assert crawler is not None, "cralwer is not defined."

		template = MentionTemplate(source=crawler)
		doc      = template.patch(raw)
		return doc