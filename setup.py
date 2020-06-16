import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="controller_storage-pkg-bghu", # Replace with your own username
    version="0.0.2",
    author="Blossom Author",
    author_email="bghuntla123@gmail.com",
    description="Maya package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/controller_storage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows 10",
    ],
    python_requires='==2.7',
)