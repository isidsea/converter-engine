class ValidationError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class ParseError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class CannotFindField(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class CannotFindDocument(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class DuplicateMention(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class NetworkTimeout(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)