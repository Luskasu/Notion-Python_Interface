from setuptools import setup, find_packages

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup(
    name="notioninterface",
    version="0.1.0",
    author="Lucas Araujo",
    author_email="lucas.araujo.barboza@gmail.com",
    description="This is a python module to conect to notion API. In a nutsheel, what it does do is just use python requests to access notion API endpoints",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Luskasu/notioninterface",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=requirements,
)

