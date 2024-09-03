from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="py_schwab_wrapper",  # This is the name that will be used for `pip install`
    version="0.2.0",  
    author="Luis Perez",
    author_email="luispe@gmail.com",
    description="A Python wrapper for Schwab API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeAndCandlesticks/py-schwab-wrapper", 
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "pytz",
        "flask",
        "requests-oauthlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)