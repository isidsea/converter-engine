from lib.object.source     import Source
from lib.factory.extractor import ExtractorFactory
from lib.factory.parser    import ParserFactory
from lib.factory.saver     import SaverFactory
from lib.exceptions		   import DuplicateMention, NetworkTimeout
from curtsies              import fmtstr
import multiprocessing

def run_converter(crawler):
	extractor = ExtractorFactory.get_extractor(ExtractorFactory.NOT_CONVERTED)
	docs      = extractor.extract(crawler)
	print("[ConverterEngine][debug] Found %s document(s)" % docs.count())

	for doc in docs:
		parser = ParserFactory.get_parser(ParserFactory.RAW_MENTION)
		mention = parser.parse(crawler, doc)

		parser = ParserFactory.get_parser(ParserFactory.AUTHOR_INFO)
		author = parser.parse(mention)
		try:
			saver = SaverFactory.get_saver(SaverFactory.MENTION)
			saver.save(mention)

			saver = SaverFactory.get_saver(SaverFactory.AUTHOR_INFO)
			saver.save(author)

			print(fmtstr("[ConverterEngine][success] Converted One Document!", "green"))
		except DuplicateMention as ex:
			print(fmtstr("[ConverterEngine][error] %s" % ex, "red"))
		except NetworkTimeout as ex:
			print(fmtstr("[ConverterEngine][error] Network Timeout.", "red"))
		finally:
			saver = SaverFactory.get_saver(SaverFactory.MENTION)
			saver.set_as_converted(crawler, mention)

if __name__ == "__main__":
	source = Source()
	with multiprocessing.Pool(20) as pool:
		pool.map(run_converter, source.crawlers)
		