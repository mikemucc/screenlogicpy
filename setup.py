import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="screenlogicpy",
    version="0.0.2",
    author="Kevin Worrel",
    author_email="kevinworrel@yahoo.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dieselrabbit/screenlogicpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
	"Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.6',
    entry_points={
            'console_scripts': [
                  'screenlogicpy=screenlogicpy.cli:cli',
            ],
      },
)