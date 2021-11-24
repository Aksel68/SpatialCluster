from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'Spatial cluster package'

# Setting up
setup(
    name="SpatialCluster",
    version=VERSION,
    author="AxelReyesO (Axel Reyes O)",
    author_email="<axel.reyes@sansano.usm.cl>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['tensorflow','scipy','numpy'],
    url="https://github.com/AxlKings/SpatialCluster",
    keywords='python spatial urban cluster',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)