from ..config.source import SourceConfig

class ConfigFactory:

	SOURCE = 0

	def __init__(self):
		pass

	@classmethod
	def get_config(self, config_name=None):
		assert config_name is not None, "config_name is not defined."

		if config_name == ConfigFactory.SOURCE:
			return SourceConfig()