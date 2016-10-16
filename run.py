from lib.object.source     import Source
from lib.factory.extractor import ExtractorFactory
from lib.factory.parser    import ParserFactory
from lib.factory.saver     import SaverFactory
from lib.exceptions		   import DuplicateMention, NetworkTimeout, ValidationError
from curtsies              import fmtstr
import multiprocessing

def run_converter(crawler):
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
			print(fmtstr("[%s][error] %s" % (crawler.name, ex), "red"))
			mention_saver = SaverFactory.get_saver(SaverFactory.MENTION)
			mention_saver.set_as_converted(crawler, mention)
		except NetworkTimeout as ex:
			print(fmtstr("[ConverterEngine][error] Network Timeout.", "red"))
		except ValidationError as ex:
			print(fmtstr("[%s][error] %s" % (crawler.name, ex),"red"))

if __name__ == "__main__":
	source = Source()
	with multiprocessing.Pool(20) as pool:
		pool.map(run_converter, source.crawlers)
		