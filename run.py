from lib.object.source     import Source
from lib.factory.extractor import ExtractorFactory
from lib.factory.parser    import ParserFactory
from lib.factory.saver     import SaverFactory
from lib.factory.logger    import LoggerFactory
from lib.exceptions		   import DuplicateMention, NetworkTimeout, ValidationError
from curtsies              import fmtstr
import multiprocessing

def run_converter(crawler):
	log_saver = SaverFactory.get_saver(SaverFactory.LOG)
	logger    = LoggerFactory.get_logger(LoggerFactory.CONVERTER)
	logger.log(level=logger.INFO, state="START", message="Converting: %s" % crawler.name)
	log_saver.save(logger)

	extractor = ExtractorFactory.get_extractor(ExtractorFactory.NOT_CONVERTED)
	docs      = extractor.extract(crawler)
	print("[ConverterEngine][debug] Found %s document(s) in %s" % (docs.count(), crawler.name))

	for doc in docs:
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
		except DuplicateMention as ex:
			try:
				print(fmtstr("[%s][error] %s" % (crawler.name, ex), "red"))
				mention_saver = SaverFactory.get_saver(SaverFactory.MENTION)
				mention_saver.set_as_converted(crawler, mention)
			except NetworkTimeout as ex:
				print(fmtstr("[ConverterEngine][error] Network Timeout.", "red"))
		except NetworkTimeout as ex:
			print(fmtstr("[ConverterEngine][error] Network Timeout.", "red"))
		except ValidationError as ex:
			print(fmtstr("[%s][error] %s" % (crawler.name, ex),"red"))

	logger.log(level=logger.INFO, state="STOP", message="Stopped: %s" % crawler.name, number_of_documents=docs.count())
	log_saver.save(logger)
if __name__ == "__main__":
	source = Source()
	with multiprocessing.Pool(20) as pool:
		pool.map(run_converter, source.crawlers)
		