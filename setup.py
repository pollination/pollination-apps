import setuptools

with open('README.md') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="pollination-apps",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="Ladybug Tools",
    author_email="info@ladybug.tools",
    description="A library to setup and deploy Apps to Pollination!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pollination/pollination-apps",
    packages=setuptools.find_packages(exclude=["tests", "docs"]),
    install_requires=requirements,
    entry_points={
        "console_scripts": ["pollination-apps = pollination_apps.cli:main"]
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    license="MIT"
)
