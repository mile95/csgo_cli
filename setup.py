import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setuptools.setup(
    name="csgo-cli",
    version="0.1.1",
    author="Fredrik Mile",
    author_email="fredrik.mile@gmail.com",
    description="CSGO CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license="LICENSE",
    url="https://github.com/mile95/csgo_cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=required,
    entry_points={
        'console_scripts': ['csgo=cli:app'],
    }
)