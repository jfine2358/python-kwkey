import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kwkey",
    version="0.0.1",
    author="Jonathan Fine",
    author_email="jfine2358@gmail.com",
    description="Indexing with keyword arguments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jfine2358/python-kwkey",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
