import setuptools
from tryhackme import __version__
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tryhackme.py",
    version=__version__,
    author="gnarlito",
    author_email="gnarlito35@gmail.com",
    description="THM public API wrapper",
    include_package_data=True,
    packages=[
        "tryhackme"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnarlito/tryhackme.py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Internet :: WWW/HTTP"
    ],
    python_requires='>=3.8',
    install_requires=[
        "requests==2.26.0"
    ],
)
