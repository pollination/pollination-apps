import os
from pathlib import Path

import click
from slugify.slugify import slugify

from ..env import Environment
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


@main.command('viz')
def viz():
    """check pollination apps is flying"""
    click.echo("""

                                       .' '.            __
  viiiiiiiiiiiiizzzzzzzzz!  . .        .   .           (__\_
                               .         .         . -{{_(|8)
                                 ' .  . ' ' .  . '     (__/

    """)

