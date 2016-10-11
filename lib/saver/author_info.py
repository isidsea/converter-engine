import pymongo

class AuthorInfoSaver:
	def __init__(self):
		pass

	def save(self, author_info=None):
		assert author_info is not None, "mention is not defined."

		conn = pymongo.MongoClient("mongodb://alex:07081984@220.100.163.138/?authSource=admin")
		db   = conn["isid"]

		try:
			db.author_info.insert_one(author_info)
		except pymongo.errors.DuplicateKeyError:
			db.author_info.update_one(
				{
				  	"AuthorScreenName": author_info["AuthorScreenName"],
					      "AuthorType": author_info["AuthorType"],
					       "AuthorId" : author_info["AuthorId"]
				},
				{
					"$inc":{"AuthorTotalMentionsCrawled":1},
					"$set":{
						   "LastUpdatedDate":author_info["LastUpdatedDate"], 
						"LastUpdatedDateISO":author_info["LastUpdatedDateISO"]
					}
				}
			)
		conn.close()