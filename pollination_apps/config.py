"""Pollination App Config"""
from dataclasses import dataclass
import configparser
import pathlib


@dataclass()
class Config:
    """Pollination app configuration.

    Args:
        name: App human readable name. e.g. My first app
        owner: App's owner on pollination. e.g. ladybug-tools

    """
    name: str
    owner: str

    @classmethod
    def from_file(cls, path: str):
        """Create a config object from a config file.

        Args:
            path: Full path to the config.ini file.

        """
        parser = configparser.ConfigParser()
        parser.read(path)
        app_info = parser['app']
        owner = app_info.get('owner')
        name = app_info.get('name')
        return cls(name, owner)

    @classmethod
    def from_folder(cls, folder: str):
        """Create a config object from an app folder.

        Args:
            folder: Path to app folder. The config file should be located at
                .pollination/config.ini

        """
        config_file = pathlib.Path(folder).joinpath('.pollination', 'config.ini')
        if not config_file.is_file():
            raise FileNotFoundError(f'Failed to find the config file: {config_file}')
        return cls.from_file(config_file.as_posix())

    def write(self, folder: str):
        """Write config to an ini file.

        Args:
            folder: Path to app folder. The config file will be created at
                .pollination/config.ini
        """
        config_file = pathlib.Path(folder).joinpath('.pollination', 'config.ini')
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config = configparser.ConfigParser()
        config.add_section('app')
        config['app']['owner'] = self.owner
        config['app']['name'] = self.name
        with config_file.open('w') as out_ini:
            config.write(out_ini)
