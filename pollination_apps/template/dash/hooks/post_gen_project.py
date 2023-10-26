"""This module performs post-generation tasks once the project is created.
These tasks may include: removing files, renaming files, etc.
"""

import os
import shutil
from pathlib import Path

# Remove .github folder if CI is not requested
REMOVE_PATHS = [
    '{% if cookiecutter.ci == "none" %} .github {% endif %}',
    '{% if cookiecutter.ci == "github-manual" %} .github/workflows/ci-automated.yaml {% endif %}',
    '{% if cookiecutter.ci == "github-manual" or cookiecutter.ci == "none" %} .gitignore {% endif %}',
    '{% if cookiecutter.ci == "github-manual" or cookiecutter.ci == "none" %} .releaserc.json {% endif %}',
    '{% if cookiecutter.ci == "github-automated" %} .github/workflows/ci-manual.yaml {% endif %}',
]

# Remove files / folders
for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)

# Rename CI if CI is requested
ci_folder = Path('.github/workflows')
ci_file_path = ci_folder.joinpath('ci.yaml')
if ci_folder.exists():
    for file_path in ci_folder.iterdir():
        file_path.rename(ci_file_path)


# If Pollination_viewer is requested, add support for vtk in the Dockerfile
vtk_docker_file_path = Path('./app/vtk.Dockerfile')
docker_file_path = Path('./app/Dockerfile')

NEEDS_VIEWER = '{% if cookiecutter.pollination_viewer == "yes" %} yes {% endif %}'
if NEEDS_VIEWER.strip() == 'yes':
    os.remove(docker_file_path.as_posix())
    vtk_docker_file_path.rename(docker_file_path)
else:
    os.remove(vtk_docker_file_path.as_posix())
