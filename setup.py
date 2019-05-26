import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HQApi",
    version="2.1.2",
    author="Katant",
    author_email="katant.savelev@yandex.ru",
    description="HQ Trivia & Words API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apipy/HQApi",
    install_requires=['requests', 'lomond', 'aws-requests-auth', 'PyJWT'],
    packages=["HQApi"],
    python_requires='>=3.4',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
