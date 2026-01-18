from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="CONSUMER GADGETS RECOMMENDER",
    version="0.1",
    author="Dani",
    packages=find_packages(),
    install_requires = requirements,
)