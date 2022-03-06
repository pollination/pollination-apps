from pathlib import Path

from cookiecutter.main import cookiecutter

TEMPLATE_PATH = Path(__file__).parent.joinpath('assets').absolute()


def generate_template(output_dir: Path):
    cookiecutter(
        template=TEMPLATE_PATH.as_posix(),
        output_dir=output_dir,
        overwrite_if_exists=True,
    )
