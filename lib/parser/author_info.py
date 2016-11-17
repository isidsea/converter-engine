import arrow
import bson.json_util

class AuthorInfoParser:
	def __init__(self):
		pass

	def parse(self, mention=None):
		""" Exceptions:
			- AssertionError
		"""
		assert mention is not None, "mention is not defined."

		update_time      = arrow.now().format("YYYY-MM-DD HH:mm:ss")
		update_time_iso  = "%sZ" % arrow.utcnow().format("YYYY-MM-DDTHH:mm:ss")
		author_info = {
			                "AuthorType" : mention.SourceName,
			                  "AuthorId" : mention.AuthorId,
			          "AuthorScreenName" : mention.AuthorName,
			         "AuthorDisplayName" : mention.AuthorDisplayName,
			            "AuthorLocation" : mention.AuthorLocation,
			       "AuthorFollowerCount" : -1,
			         "AuthorFriendCount" : -1,
			         "AuthorStatusCount" : -1,
			            "AuthorLanguage" : "",
			"AuthorTotalMentionsCrawled" : 1,
			           "LastUpdatedDate" : update_time,
			        "LastUpdatedDateISO" : update_time_iso.replace(" ","T")
		}
		return author_info