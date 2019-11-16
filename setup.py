import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robot",
    version='0.3.1',
    author="Sherevv",
    author_email="sherevv@gmail.com",
    description="Robot on the cave field",
    long_description=long_description,
    include_package_data=True,
    url="https://github.com/sherevv/robot",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'numpy==1.17.4',
        'matplotlib==3.1.1'
    ]
)