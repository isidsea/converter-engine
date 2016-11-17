from raven.conf 		    import setup_logging
from raven.handlers.logging import SentryHandler
import raven
import logging

class Logger(raven.Client):
	def __init__(self, **kwargs):
		self.public_key = "c315978776e34ccc816da619bc3c2f28"
		self.secret_key = "56fa120c52db4bdd95c910ae2d251128"
		self.project_id = 3

		self.dsn = "http://%s:%s@sentry:9000/%s" % (
			self.public_key,
			self.secret_key,
			self.project_id
		)
		raven.Client.__init__(self, self.dsn, auto_log_stacks=True, **kwargs)

		self.handler = SentryHandler(self)
		setup_logging(self.handler)