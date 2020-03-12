from setuptools import setup

setup(
    name='mashup',
    packages=['mashup'],
    include_package_data=True,
    install_requires=[
        'quart',
        'aiohttp'
    ],
)
