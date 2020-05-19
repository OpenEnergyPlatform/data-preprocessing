import setuptools
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "..", "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oem2orm",
    version="0.1.0",
    author="henhuy, jh-RLI",
    author_email="Hendrik.Huyskens@rl-institut.de",
    description="SQLAlchemy module to create ORM, read from data model in open-energy-metadata(oem-v1.4.0) JSON format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenEnergyPlatform/data-preprocessing/tree/feature/oep-upload-oem2orm/data-import/oep-upload",
    packages=setuptools.find_packages(),
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: AGPL-3.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['sqlalchemy'],  # Optional
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/OpenEnergyPlatform/data-preprocessing/issues',
        'Source': 'https://github.com/OpenEnergyPlatform/data-preprocessing/tree/feature/oep-upload-oem2orm/data-import/oep-upload/oem2orm',
    },
)