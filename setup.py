from distutils.core import setup

import setuptools

extras_require = {
    "test": [
        "black",
        "ruff",
        "mypy",
        "pytest",
    ],
}
extras_require["dev"] = ["pre-commit", *extras_require["test"]]
all_require = [r for reqs in extras_require.values() for r in reqs]
extras_require["all"] = all_require


setup(
    name="swingsage",
    version="1.0.0",
    author="Ryan Smith",
    author_email="ryanmsmith251@gmail.com",
    url="https://github.com/rmsmith251/SwingSage",
    packages=setuptools.find_packages(exclude=["tests"]),
    description="project_description",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "pydantic",
        "torch",
        "torchvision",
        "transformers",
        "SQLAlchemy",
    ],
    extras_require=extras_require,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
