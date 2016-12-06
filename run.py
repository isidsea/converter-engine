from lib.object.source     import Source
from lib.factory.extractor import ExtractorFactory
from lib.factory.parser    import ParserFactory
from lib.factory.saver     import SaverFactory
from lib.logger            import Logger
from lib.exceptions		   import DuplicateMention, NetworkTimeout, ValidationError, CannotFindDocument
from curtsies              import fmtstr
import multiprocessing
import logging

def run_converter(crawler):
	""" Exceptions:
		- AssertionError (RawMentionParser, AuthorInfoParser, MentionSaver, AuthorInfoSaver)
	"""
	logger    = logging.getLogger(__name__)

	try:
		extractor = ExtractorFactory.get_extractor(ExtractorFactory.NOT_CONVERTED)
		docs      = extractor.extract(crawler)
		number_of_document = docs.count()
	except CannotFindDocument as ex:
		docs 			   = []
		number_of_document = 0
	print("[ConverterEngine][debug] Found %s document(s) in %s" % (number_of_document, crawler.name))

	with multiprocessing.Pool(10) as pool:
		pool.map(batch_convert, docs)
		
def batch_convert(doc):
	mention = None
	try:
		parser  = ParserFactory.get_parser(ParserFactory.RAW_MENTION)
		mention = parser.parse(crawler, doc)

		parser = ParserFactory.get_parser(ParserFactory.AUTHOR_INFO)
		author = parser.parse(mention)

		mention_saver = SaverFactory.get_saver(SaverFactory.MENTION)
		mention_saver.save(mention)

		author_saver = SaverFactory.get_saver(SaverFactory.AUTHOR_INFO)
		author_saver.save(author)

		mention_saver.set_as_converted(crawler, mention)
		print(fmtstr("[%s][success] Converted One Document!" % crawler.name, "green"))
	except ValidationError as ex:
		logger.error(str(ex), exc_info=True)
	except DuplicateMention as ex:
		if mention is not None:
			mention_saver.set_as_converted(crawler, mention)
		print(fmtstr("[%s][success] Ops! Duplicate document" % crawler.name, "red"))
	except NetworkTimeout as ex:
		logger.error(str(ex), exc_info=True)

if __name__ == "__main__":
	Logger()
	source = Source()
	run_converter(source.crawlers[0])
		