from setuptools import setup, find_packages

from clyjin import __version__ as version


with open("requirements.txt", "r") as file:
    install_requires = [x.strip() for x in file.readlines()]

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="clyjin",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description="System configuration toolbox",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Alexander Ryzhov",
    author_email="thed4rkof@gmail.com",
    url="https://github.com/ryzhovalex/clyjin",
    keywords=["cli", "automatization", "system", "os"],
    entry_points={
        "console_scripts": [
            "clyjin = clyjin.core.cli:main",
            "cj = clyjin.core.cli:main"
        ],
    },
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 1 - Planning",

        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3.7",
    ],
)
