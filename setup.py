from setuptools import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="get_fshare",
    version="2.5.0",
    description="Python lib to get link Fshare.vn",
    url="http://github.com/tudoanh/get_fshare",
    author="Do Anh Tu",
    author_email="tu0703@gmail.com",
    license="MIT",
    packages=["get_fshare"],
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
)
