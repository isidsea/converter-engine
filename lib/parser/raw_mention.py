from ..factory.validator import ValidatorFactory
from ..template.mention  import MentionTemplate
from ..exceptions        import ParseError
from urllib.parse        import urlparse
import arrow
import hashlib

class RawMentionParser:
	def __init__(self):
		pass


	def parse(self, crawler=None, raw=None):
		assert raw     is not None, "raw is not defined."
		assert crawler is not None, "cralwer is not defined."

		validator = ValidatorFactory.get_validator(ValidatorFactory.RAW_MENTION)
		validator.validate(raw)

		_id               = raw["permalink"] if "permalink" in raw else raw["url"] if "url" in raw else None
		mention_misc_info = raw["_thread_link"] if "_thread_link" in raw else ""
		author_id         = raw["author_id"] if "author_id" in raw else raw["author_name"] if "author_name" in raw else raw["author"] if "author" in raw else ""
		author_name       = raw["author_name"] if "author_name" in raw else raw["author"] if "author" in raw else ""
		country           = raw["_country"] if "_country" in raw else raw["country"] if "country" in raw else ""

		source_name  = raw["permalink"]
		source_name  = urlparse(source_name).netloc.lower().replace("www.","")
		source_name  = "%s%s" % (source_name[0].upper(), source_name[1:])
		mention_type = "{}_post" if crawler.type == "Blogs" or crawler.type == "Forums" else "{}_article" if crawler.type == "News" else source_name
		mention_type = mention_type.format(source_name)
		mention_type = mention_type.lower()

		template = MentionTemplate(source=crawler)
		template.MentionId   				  = hashlib.sha256(_id.encode("utf-8")).hexdigest()
		template.MentionText 			  	  = raw["content"]
		template.MentionMiscInfo 			  = mention_misc_info
		template.MentionType     			  = mention_type 
		template.MentionDirectLink 			  = raw["permalink"]
		template.MentionCreatedDate 		  = raw["published_date"]
		template.MentionCreatedDateISO 		  = raw["published_date"]
		template.AuthorId                     = author_id
		template.AuthorName                   = author_name
		template.AuthorDisplayName            = author_name
		template.SourceType                   = crawler.type
		template.SourceName                   = source_name
		template.SentFromHost                 = "220.100.163.132"
		template.SentFromCrawler              = crawler.name
		template.DateInsertedIntoCrawlerDB    = raw["_insert_time"]
		template.DateInsertedIntoCrawlerDBISO = raw["_insert_time"]
		template.DateInsertedIntoCentralDB    = arrow.now().datetime
		template.DateInsertedIntoCentralDBISO = arrow.utcnow().datetime
		template.Country                      = country
		return template