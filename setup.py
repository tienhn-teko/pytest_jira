# coding=utf-8
import setuptools

with open("README.md", "r", encoding="utf8") as rm:
    README = rm.read()


setup_args = dict(
    name='pytest-jira',
    version_format='{tag}.dev{commitcount}+{gitsha}',
    setup_requires=['setuptools-git-version'],
    long_description=README,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url='https://github.com/tienhn-teko/pytest-jira',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)

install_requires = [
    'docstring_parser',
    'request'
]

setuptools.setup(
    **setup_args,
    install_requires=install_requires)