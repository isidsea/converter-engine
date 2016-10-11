from ..exceptions import ValidationError

class RawMentionValidator:
	def __init__(self):
		pass

	def validate(self, raw=None):
		assert raw is not None, "raw is not defined."

		if "permalink" not in raw and "url" not in raw:
			raise ValidationError("Cannot find permalink or url inside raw.")

		if "author" not in raw and "author_name" not in raw:
			raise ValidationError("Cannot find author or author_name inside raw.")

		if "content" not in raw:
			raise ValidationError("Cannot find content.")

		if "published_date" not in raw:
			raise ValidationError("Cannot find published_date.")

		if "_insert_time" not in raw:
			raise ValidationError("Cannot find _insert_time.")

		if "_country" not in raw and "country" not in raw:
			raise ValidationError("Cannot find _country.")
			