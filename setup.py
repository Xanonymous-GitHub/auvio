from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="auvio",
    version="1.0.4",
    author="NPC OwO",
    author_email="support@ntut.club",
    description="Let your zuvio roll the call automatically, "
                "don’t get up for roll call anymore, give yourself a good morning!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xanonymous-GitHub/auvio",
    packages=['auvio'],
    platforms=["all"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    install_requires=['requests', 'bs4', 'beautifulsoup4'],
)
