import tarfile
import tempfile
from pathlib import Path

import pollination_sdk as sdk
import requests


class APIClient(object):
    """A Pollination client designed to interact with Workflow and Simulation objects."""

    def __init__(self, api_token=None, access_token=None, host='https://api.pollination.cloud'):
        self.config = sdk.Configuration()
        if api_token is not None:
            self.set_api_token(api_token)
        elif access_token is not None:
            self.set_jwt(access_token)

        self.set_host(host)

        self.auth = sdk.UserApi(sdk.ApiClient(self.config))
        self.api_tokens = sdk.APITokensApi(sdk.ApiClient(self.config))
        self.applications = sdk.ApplicationsApi(sdk.ApiClient(self.config))

    def set_host(self, host: str):
        self.config.host = host

    def set_jwt(self, jwt: str):
        self.config.api_key = {}
        self.config.access_token = jwt

    def set_api_token(self, api_token: str):
        self.config.api_key = {'APIKeyAuth': api_token}
        self.config.access_token = None

    def get_account(self) -> sdk.UserPrivate:
        return self.auth.get_me()

    def create_api_token(self) -> str:
        token: sdk.APITokenPrivate = self.api_tokens.create_token(
            api_token_create=sdk.APITokenCreate(
                token_id='pollination-apps-cli',
                name='pollination-apps-cli'
            )
        )
        return token.token

    def get_app(self, owner: str, slug: str) -> sdk.Application:
        return self.applications.get_application(
            owner=owner,
            slug=slug,
        )

    def create_app(self, owner: str, name: str, public: bool = True):
        self.applications.create_application(
            owner=owner,
            application_create=sdk.ApplicationCreate(
                name=name,
                public=public,
            )
        )

    def update_app(self, owner: str, slug: str, public: bool):
        self.applications.update_application(
            owner=owner,
            slug=slug,
            application_update=sdk.ApplicationUpdate(
                public=public,
            )
        )

    def get_upload_link(self, owner: str, slug: str, tag: str, release_notes: str = '') -> sdk.S3UploadRequest:
        return self.applications.upsert_application_version(
            owner=owner, slug=slug,
            new_application_version=sdk.NewApplicationVersion(
                tag=tag,
                release_notes=release_notes,
            )
        )

    def upload_app_folder(self, link: sdk.S3UploadRequest, path: Path):
        file = Path(tempfile.mktemp())
        with tarfile.open(file, mode="w:gz") as tar:
            for p in path.iterdir():
                tar.add(p, arcname=p.name)

        requests.post(
            link.url, data=link.fields,
            files={'file': open(file, 'rb')}
        )
