import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loadshedding", # Replace with your own username
    version="1.1.1",
    author="Wilson Kuo",
    author_email="wilson.kuo@acspower.com",
    install_requires=["acstw"],
    description="loadshedding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    package_data={'': ['*.sql']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


# python3 setup.py sdist
# python3 -m pip install ./dist/loadshedding-1.1.1.tar.gz --user
# python3 setup.py sdist; python3 -m pip install ./dist/loadshedding-1.1.1.tar.gz --user;