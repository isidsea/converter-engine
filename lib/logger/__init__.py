class Logger:
	DEBUG = 0
	INFO  = 1
	
	def __init__(self):
		self.logs       = []
		self.saved_logs = []