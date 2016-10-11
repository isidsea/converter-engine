class Crawler:
	def __init__(self, **kwargs):
		self.type = kwargs.get("type", None)
		self.name = kwargs.get("name",None)
		self.db   = kwargs.get("db",None)