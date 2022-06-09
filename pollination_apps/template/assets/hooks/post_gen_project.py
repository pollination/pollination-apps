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
NEEDS_VIEWER = '{% if cookiecutter.pollination_viewer == "yes" %} yes {% endif %}'
if NEEDS_VIEWER.strip() == 'yes':
    docker_file_path = Path('./app/Dockerfile')
    with open(docker_file_path, 'r') as f:
        docker_file_data = f.readlines()

    vtk_support = [
        'RUN apt-get update \\ \n',
        '\t&& apt-get -y install ffmpeg libsm6 libxext6 xvfb --no-install-recommends \\ \n',
        '\t&& apt-get clean \\ \n',
        '\t&& rm -rf /var/lib/apt/lists/* \n',
        '\n',
    ]

    new_docker_file_data = docker_file_data[0:2] + vtk_support + docker_file_data[2:]
    with open(docker_file_path, 'w') as f:
        f.writelines(new_docker_file_data)
