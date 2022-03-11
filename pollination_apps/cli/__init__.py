import os
import subprocess
import signal
from pathlib import Path

import click
from click import ClickException
from slugify.slugify import slugify

from ..env import Environment
from ..template import generate_template
from .context import Context

from..login import interactive_login

MODULE_PATH = os.path.abspath(os.path.dirname(__file__))


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
    '-t', '--token-name', help='the name of the api tokern created for this client',
    default='pollination-apps-cli',
)
def login(environment: str, token_name: str):
    """login to pollination"""

    ctx = Context.from_file()
    env = Environment.from_string(environment)
    jwt = interactive_login(url=env.login_url)
    client = ctx.client
    client.set_host(env.api_host)
    client.set_jwt(jwt)
    user = client.get_account()
    if client.api_token_name_exists(name=token_name):
        raise click.ClickException(
            f'Login Failed -> API Token name {token_name} is already taken. '
            'You can either:\n'
            f'\t1. delete it from the web application at https://app.pollination.cloud/{user.username}?tab=settings\n'
            '\t2. choose a new name by using the --token-name/-t flag'
        )
    ctx.api_token = client.create_api_token(name=token_name)
    ctx.save()


@main.command('deploy')
@click.argument('path', type=click.Path(exists=True))
@click.option('-o', '--owner', help='the owner of the app on pollination (defaults to logged in user)')
@click.option('-n', '--name', help='the name of the app (defaults to folder name)')
@click.option('-t', '--tag', help='the tag for this version of the app')
@click.option(
    '-m', '--message', help='the commit message for this version of the app', show_default=True,
    default='The best version of this app... so far!'
)
@click.option(
    '-e', '--environment', help='the pollination environment',
    type=click.Choice(['staging', 'production']),
    default='production'
)
@click.option(
    '--public/--private', help='Indicate if the application should be created as '
    'a public or a private resource. This option does not change the visibility of a '
    'resource if it already exist.', is_flag=True, default=True
)
@click.option(
    '--pollination/--local', help='A flag to change between deploying the app to '
    'Pollination or locally. The local option is useful for testing and debugging the '
    'app. To use the local deployment you must have Docker installed locally.',
    is_flag=True, default=True
)
def deploy(path, owner, name, tag, message, environment, public, pollination):
    """deploy a new application version"""
    ctx = Context.from_file()

    client = ctx.client
    env = Environment.from_string(environment)
    client.set_host(env.api_host)
    user = client.get_account()

    if owner is None:
        owner = user.username

    path = Path(path).absolute()
    if name is None:
        name = path.name

    for required_file in ('Dockerfile', 'app.py'):
        if not path.joinpath(required_file).is_file():
            raise ClickException(
                f'Application folder is missing a required file: {required_file}'
            )

    slug = slugify(name)

    if tag is None:
        tag = 'latest'

    if pollination:
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
            'It can take a few minutes before the new version of the app is deployed to '
            'Pollination. You can check the app at this URL: '
            f'{base_url}/{owner}/applications/{slug}'
        )
    else:
        docker_file = path.joinpath('Dockerfile')
        build_image = f'docker build -f {docker_file} -t {owner}/{slug}:{tag} {path}'
        run_app = f'docker run -t -i --expose 8501 -p 8501:8501 {owner}/{slug}:{tag} streamlit run app.py'
        click.echo(f'Building an image for {owner}/{slug}:{tag}')
        rc = subprocess.call(build_image.split())
        if rc != 0:
            ClickException('Failed to build the image.')
        click.echo(f'Starting the {name} app at http://localhost:8501/')

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


@main.command('new')
def new():
    """create a new app"""
    output_dir = Path(os.getcwd())
    generate_template(output_dir)
