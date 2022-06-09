"""This module performs post-generation tasks once the project is created.
These tasks may include: removing files, renaming files, etc.
"""

import os
import shutil
from pathlib import Path

# Remove .github folder if CI is not requested
REMOVE_PATHS = [
    '{% if cookiecutter.ci != "github-actions" %} .github {% endif %}',
]
for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)


# If Pollination_viewer is requested, add support for vtk in the Dockerfile
vtk_docker_file_path = Path('./app/vtk.Dockerfile')
docker_file_path = Path('./app/Dockerfile')

NEEDS_VIEWER = '{% if cookiecutter.pollination_viewer == "yes" %} yes {% endif %}'
if NEEDS_VIEWER.strip() == 'yes':
    os.remove(docker_file_path.as_posix())
    vtk_docker_file_path.rename(docker_file_path)
else:
    os.remove(vtk_docker_file_path.as_posix())
