from setuptools import setup, find_packages

setup(
    name='schwab_api_wrapper',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'requests_oauthlib',
    ],
    description='A Python wrapper for Schwab Developer APIs',
    author='Luis Perez',
    author_email='luispe@gmail.com',
    url='https://github.com/CodeAndCandlesticks/py-schwab-wrapper',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
