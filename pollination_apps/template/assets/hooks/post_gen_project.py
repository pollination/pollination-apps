import os
import shutil

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
