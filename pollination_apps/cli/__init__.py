import os
import pathlib
import subprocess
import signal
from pathlib import Path

import click
from click import ClickException
from slugify.slugify import slugify

from ..env import Environment
from ..template import generate_template
from .context import Context
from ..config import Config


MODULE_PATH = os.path.abspath(os.path.dirname(__file__))


def _slugify(name):
    """An internal function to slugify names."""
    return slugify(name, replacements=[['_', '-']])


@click.group(invoke_without_command=True)
@click.version_option()
@click.pass_context
def main(ctx: click.Context):
    """ The Pollination Apps CLI

    Use this CLI to create a new app and deploy it to Pollination.

    Try ``pollination-apps new`` and follow the directions for developing the app
    and deploying your first app to Pollination.

    """
    if ctx.invoked_subcommand is None:
        with open(os.path.join(MODULE_PATH, 'assets/art.txt'), 'r') as f:
            queenbee_art = f.read()
        click.echo(queenbee_art)
        click.echo(ctx.command.get_help(ctx))


@main.command('login')
@click.option(
    '-e', '--environment', help='the pollination environment',
    type=click.Choice(['staging', 'production']),
    default='production'
)
@click.option(
    '-t', '--token-name', help='the name of the api token created for this client',
    default='pollination-apps-cli',
)
def login(environment: str, token_name: str):
    """login to pollination"""
    msg = 'The login command has been deprecated. Try to set the value using the ' \
        'POLLINATION_TOKEN environmental variable or pass the API key to the commands ' \
        'directly using the --api-token option.'

    raise ClickException(msg)


@main.command('deploy')
@click.argument('path', type=click.Path(exists=True))
@click.option('-o', '--owner', help='the owner of the app on pollination.')
@click.option('-n', '--name', help='the name of the app.')
@click.option('-t', '--tag', help='the tag for this version of the app')
@click.option(
    '-m', '--message', help='the commit message for this version of the app', show_default=True,
    default='A new version of the app.'
)
@click.option(
    '-e', '--environment', help='the pollination environment',
    type=click.Choice(['staging', 'production']),
    default='production', show_default=True
)
@click.option(
    '--public/--private', help='Indicate if the application should be created as '
    'a public or a private resource. This option does not change the visibility of a '
    'resource if it already exist.', is_flag=True, default=True, show_default=True
)
@click.option(
    '-at', '--api-token', type=str, help='A valid Pollination API token', default=None,
    show_default=True
)
def deploy(path, owner, name, tag, message, environment, public, api_token):
    """Deploy a new version of the application.

    \b
    Args:
        path: Full path to apps folder.
    """

    if api_token:
        ctx = Context(api_token=api_token)
    else:
        ctx = Context()

    if not ctx.api_token:
        raise ClickException(
            'Either provide an API key using --api-token or make sure the API key is'
            ' assigned to your environment variable POLLINATION_TOKEN'
        )

    client = ctx.client
    env = Environment.from_string(environment)
    client.set_host(env.api_host)

    path = Path(path).absolute()

    for required_file in ('Dockerfile', 'app.py'):
        if not path.joinpath(required_file).is_file():
            raise ClickException(
                f'Application folder is missing a required file: {required_file}'
            )

    owner, name, slug = _read_config(path, owner, name)
    slug = slug or _slugify(name)

    if tag is None:
        tag = 'latest'

    try:
        client.update_app(owner=owner, slug=slug, public=public)
    except:
        client.create_app(owner, name, public)

    upload_link = client.get_upload_link(
        owner=owner,
        slug=slug,
        tag=tag,
        release_notes=message,
    )

    client.upload_app_folder(
        link=upload_link,
        path=path,
    )

    base_url = 'https://app.staging.pollination.cloud' if environment == 'staging' \
        else 'https://app.pollination.cloud'

    click.echo(
        f'\nCongrats! The "{name}" app is successfully scheduled for deployment.\n'
        'It can take up to 10 minutes before the new version of the app is deployed to '
        'Pollination. You can check the app at this URL: '
        f'{base_url}/{owner}/apps/{slug}'
    )


@main.command('new')
@click.option(
    '-p', '--path', type=click.Path(file_okay=False),
    help='Path to the app directory. If the directory does not exist, a new directory '
    'will be created.'
)
def new(path):
    """create a new app"""
    output_dir = Path(path) if path else Path(os.getcwd())
    output_dir.mkdir(parents=True, exist_ok=True)
    generate_template(output_dir)


@main.command('run')
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
@click.option('-o', '--owner', help='The owner of the app on pollination. e.g. ladybug-tools')
@click.option('-n', '--name', help='The name of the app.')
@click.option('-t', '--tag', help='The tag for this version of the app')
@click.option('-e', '--editable', help='An option to set the container to be editable '
              'by mounting the app path as a volume to the docker container. ', 
              default=False, show_default=True, is_flag=True)
@click.option('--docker/--podman', help='An option to set the preferred container '
              'technology. The default is set to docker. You can also use podman as '
              'an alternative.', show_default=True, is_flag=True, default=True)
def run(path, owner, name, tag, editable, docker):
    """Build and run the application locally.

    \b
    Args:
        path: Full path to apps folder.

    """
    path = pathlib.Path(path)

    for required_file in ('Dockerfile', 'app.py'):
        if not path.joinpath(required_file).is_file():
            raise ClickException(
                f'Application folder is missing a required file: {required_file}'
            )

    owner, name, slug = _read_config(path, owner, name)

    slug = slug or _slugify(name)

    if tag is None:
        tag = 'latest'

    # optionally mount the current path as a volume to the container
    volume = f'-v {path}/:/app' if editable else ''
    container_manager = 'docker' if docker else 'podman'
    docker_file = path.joinpath('Dockerfile')
    build_image = f'{container_manager} build -f {docker_file} -t {owner}/{slug}:{tag} {path}'
    run_app = f'{container_manager} run -t -i --expose 8501 -p 8501:8501 {volume} {owner}/{slug}:{tag} streamlit run app.py'
    click.echo(f'Building an image for {owner}/{slug}:{tag}')

    p = subprocess.Popen(
        build_image.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    for line in iter(p.stdout.readline, b''):
        msg = line.decode('utf-8').strip()
        click.echo(msg)

    p.communicate()

    if p.returncode != 0:
        raise ClickException(
            'Failed to build the image. See the logs for the error message.'
        )

    click.echo(
        f'Starting the {name} app at http://localhost:8501/\n'
        'Click on the link above if the app does not start automatically.'
    )

    p = subprocess.Popen(
        run_app.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    for line in iter(p.stdout.readline, b''):
        msg = line.decode('utf-8').strip()
        click.echo(msg)

    try:
        p.communicate()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)


def _read_config(path, owner, name):
    try:
        config = Config.from_folder(folder=path)
    except FileNotFoundError:
        if not owner:
            raise ClickException(
                'To deploy or run an app without a config file you must provide an owner.'
            )
        if not name:
            raise ClickException(
                'To deploy or run an app without a config file you must provide a name.'
            )
        # create a config file
        config = Config(name=name, owner=owner)
        config.write(folder=path)
    else:
        owner = config.owner
        name = config.name

    slug = _slugify(name)
    return owner, name, slug
