class Database:
	def __init__(self, **kwargs):
		self.host       = kwargs.get("host", None)
		self.name       = kwargs.get("name", None)
		self.port       = kwargs.get("port", None)
		self.collection = kwargs.get("collection", None)