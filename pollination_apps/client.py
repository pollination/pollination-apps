import tarfile
import tempfile
from pathlib import Path

import pollination_sdk as sdk
import requests


class APIClient(object):
    """A Pollination client designed to interact with Workflow and Simulation objects."""

    def __init__(self, api_token=None, access_token=None, host='https://api.pollination.solutions'):
        self.config = sdk.Configuration()
        if api_token is not None:
            self.set_api_token(api_token)
        elif access_token is not None:
            self.set_jwt(access_token)

        self.set_host(host)
        self._sdk_client = sdk.ApiClient(self.config)

        self.auth = sdk.UserApi(self._sdk_client)
        self.api_tokens = sdk.APITokensApi(self._sdk_client)
        self.applications = sdk.ApplicationsApi(self._sdk_client)

    def set_host(self, host: str):
        self.config.host = host

    def set_jwt(self, jwt: str):
        self.config.api_key = {}
        self.config.access_token = jwt

    def set_api_token(self, api_token: str):
        self.config.api_key = {'APIKeyAuth': api_token}
        self.config.access_token = None

    def _get_auth_headers(self) -> dict:
        headers = {}
        self._sdk_client.update_params_for_auth(
            headers, None, ['APIKeyAuth', 'JWTAuth'])
        return headers

    def get_account(self) -> sdk.UserPrivate:
        return self.auth.get_me()

    def api_token_name_exists(self, name: str) -> bool:
        token_list: sdk.APITokenList = self.api_tokens.list_tokens()
        for token in token_list.resources:
            token: sdk.APIToken
            if token.name == name:
                return True
        return False

    def create_api_token(self, name: str) -> str:
        token: sdk.APITokenPrivate = self.api_tokens.create_token(
            api_token_create=sdk.APITokenCreate(
                token_id='pollination-apps-cli',
                name=name,
            )
        )
        return token.token

    def get_app(self, owner: str, slug: str) -> sdk.Application:
        return self.applications.get_application(
            owner=owner,
            slug=slug,
        )

    def create_app(self, owner: str, name: str, public: bool = True, app_sdk: str = 'streamlit'):
        self.applications.create_application(
            owner=owner,
            application_create=sdk.ApplicationCreate(
                name=name,
                public=public,
                sdk=app_sdk,
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

    def create_app_version(self, owner: str, slug: str, tag: str, release_notes: str = '') -> sdk.S3UploadRequest:
        return self.applications.upsert_application_version(
            owner=owner, slug=slug,
            new_application_version=sdk.NewApplicationVersion(
                tag=tag,
                release_notes=release_notes,
            )
        )

    def upload_app_folder(self, owner: str, slug: str, tag: str, path: Path):
        file = Path(tempfile.mktemp())
        with tarfile.open(file, mode="w:gz") as tar:
            for p in path.iterdir():
                tar.add(p, arcname=p.name)

        url = f'{self.config.host}/applications/{owner}/{slug}/versions/{tag}'

        auth_headers = self._get_auth_headers()

        res = requests.post(
            url=url,
            files={'file': open(file, 'rb')},
            headers=auth_headers,
            timeout=60,
        )

        res.raise_for_status()
