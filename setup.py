from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

setup(
    name='mypwd',
    version=version,
    author='Jaroslav Beran',
    author_email='jaroslav.beran@gmail.com',
    description='Very simple password manager for my python projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/berk76/mypwd',
    project_urls={
        "Bug Tracker": "https://github.com/berk76/mypwd/issues"
    },
    license='GPL-3.0',
    packages=find_namespace_packages(include=['mypwd', 'mypwd.*']),
    install_requires=requirements,
)
