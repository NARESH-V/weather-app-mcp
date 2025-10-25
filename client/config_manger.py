import os


class ConfigManager:
    _config = {}

    @staticmethod
    def load_config():
        config_path = f"client/env.py"

        local_config = {}
        with open(config_path) as f:
            exec(f.read(), local_config)

        ConfigManager._config = local_config

    @staticmethod
    def get_config(param):
        return ConfigManager._config.get(param)


ConfigManager.load_config()