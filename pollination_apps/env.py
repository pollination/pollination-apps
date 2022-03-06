from enum import Enum


class EnvironmentEnum(str, Enum):
    staging = 'staging'
    production = 'production'


class Environment:

    def __init__(self, env: EnvironmentEnum):
        self._env = env

    @classmethod
    def from_string(cls, env: str):
        return cls(EnvironmentEnum(env))

    @property
    def api_host(self) -> str:
        if self._env == EnvironmentEnum.staging:
            return 'https://api.staging.pollination.cloud'
        else:
            return 'https://api.pollination.cloud'

    @property
    def login_url(self) -> str:
        if self._env == EnvironmentEnum.staging:
            return 'https://auth.staging.pollination.cloud/sdk-login'
        return 'https://auth.pollination.cloud/sdk-login'
