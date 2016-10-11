from ..parser.raw_mention import RawMentionParser
from ..parser.author_info import AuthorInfoParser

class ParserFactory:
	RAW_MENTION = 0
	AUTHOR_INFO = 1

	def __init__(self):
		pass

	@classmethod
	def get_parser(self, parser_name=None):
		assert parser_name is not None, "parser_name is not defined."

		if parser_name == ParserFactory.RAW_MENTION:
			return RawMentionParser()
		elif parser_name == ParserFactory.AUTHOR_INFO:
			return AuthorInfoParser()