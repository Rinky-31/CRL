from setuptools import setup, find_packages

setup(
    name="crlib",
    version="0.4.4",
    author="Rinky-31",
    packages=find_packages(),
    extras_require={"balance": "chempy"},
    python_requires=">=3.10.3",
)