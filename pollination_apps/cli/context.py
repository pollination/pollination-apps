import os
import typing as t
from pathlib import Path

import click
import pollination_sdk as sdk
from pydantic import BaseModel, Field

from ..client import APIClient

DEFAULT_CONFIG_DIR = Path.home() / '.pollination'
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / 'apps.config.json'


class Context(BaseModel):

    api_token: str = Field(
        os.getenv('POLLINATION_TOKEN'),
        description='The API token to use to authenticate a user'
    )

    @classmethod
    def from_file(cls):
        os.makedirs(DEFAULT_CONFIG_DIR, exist_ok=True)
        try:
            return cls.parse_file(DEFAULT_CONFIG_PATH)
        except:
            ctx = cls()
            ctx.save()
            return ctx

    def save(self):
        DEFAULT_CONFIG_PATH.write_text(self.json())

    @property
    def client(self) -> APIClient:
        return APIClient(api_token=self.api_token)

    def try_login(self) -> sdk.UserPrivate:
        try:
            return self.client.get_account()
        except:
            raise click.ClickException(
                f'Not authenticated: {self.client.config.host}'
            )
