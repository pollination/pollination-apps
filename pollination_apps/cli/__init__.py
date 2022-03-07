import os
from pathlib import Path

import click
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
def login(environment):
    """login to pollination"""

    ctx = Context.from_file()
    env = Environment.from_string(environment)
    jwt = interactive_login(url=env.login_url)
    client = ctx.client
    client.set_host(env.api_host)
    client.set_jwt(jwt)
    ctx.api_token = client.create_api_token()
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
    '--public/--private', help='Indicate if the recipe or plugin should be created as '
    'a public or a private resource. This option does not change the visibility of a '
    'resource if it already exist.', is_flag=True, default=True
)
def deploy(path, owner, name, tag, message, environment, public):
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

    slug = slugify(name)

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


@main.command('new')
def new():
    """create a new app"""
    output_dir = Path(os.getcwd())
    generate_template(output_dir)
