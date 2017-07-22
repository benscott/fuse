from setuptools import setup

setup(
    name='fuse',
    version='0.0.1',
    description='Fuse Framework',
    author='Ben Scott',
    author_email='ben@benscott.co.uk',
    packages=[
        'fuse',
        'fuse.api',
        'fuse.schema',
        'fuse.application'
    ],
    install_requires=[],
)
