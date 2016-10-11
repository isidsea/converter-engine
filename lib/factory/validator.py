from ..validator.raw_mention import RawMentionValidator

class ValidatorFactory:
	RAW_MENTION = 0

	def __init__(self):
		pass

	@classmethod
	def get_validator(self, validator_name=None):
		assert validator_name is not None, "validator_name is not defined."

		if validator_name == ValidatorFactory.RAW_MENTION:
			return RawMentionValidator()