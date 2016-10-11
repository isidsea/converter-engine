from ..saver.mention     import MentionSaver
from ..saver.author_info import AuthorInfoSaver

class SaverFactory:
	MENTION     = 0
	AUTHOR_INFO = 1

	def __init__(self):
		pass

	@classmethod
	def get_saver(self, saver_name=None):
		assert saver_name is not None, "saver_name is not defined."

		if saver_name == SaverFactory.MENTION:
			return MentionSaver()
		elif saver_name == SaverFactory.AUTHOR_INFO:
			return AuthorInfoSaver()