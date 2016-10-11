from . import Config
import os

class SourceConfig(Config):
	def __init__(self):
		Config.__init__(self, os.path.join(".","config","source.json"))