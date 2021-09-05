from setuptools import setup, find_packages

setup(
    name="cookie",
    packages=find_packages(include=["cookie","cookie.*"]),
    install_requires=[
        "numpy",
        "graphviz"
    ]
)
