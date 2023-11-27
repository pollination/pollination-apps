from pathlib import Path

from cookiecutter.main import cookiecutter

TEMPLATE_PATH = Path(__file__).parent.absolute()


def generate_template(sdk: str, output_dir: Path):
    """Generate a new app template using the specified SDK."""
    cookiecutter(
        template=TEMPLATE_PATH.joinpath(sdk).as_posix(),
        output_dir=output_dir,
        overwrite_if_exists=True,
    )

def generate_template_non_interactive(sdk: str, output_dir: Path, context: dict):
    """Generate a new app template using the specified SDK."""
    cookiecutter(
        template=TEMPLATE_PATH.joinpath(sdk).as_posix(),
        output_dir=output_dir,
        overwrite_if_exists=True,
        no_input=True,
        extra_context=context
    )
