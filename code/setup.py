from setuptools import setup, find_packages
import codecs
import os

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.72'
DESCRIPTION = 'Spatial cluster package'

# Setting up
setup(
    name="SpatialCluster",
    version=VERSION,
    author="AxelReyesO (Axel Reyes O)",
    author_email="<axel.reyes@sansano.usm.cl>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['scikit-learn','tensorflow','scipy','numpy','matplotlib','folium','minisom','seaborn','geopandas','contextily'],
    url="https://github.com/AxlKings/SpatialCluster",
    keywords='python spatial urban cluster',
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    include_package_data=True,
    package_data={'': ['data/*.csv']},
)