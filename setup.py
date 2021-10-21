from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [
    'pdfrw',
    'pdf2image',
    'Pillow',
    ]

setup(
    name='fillpdf',
    packages=find_packages(exclude=['tests']),
    version='0.3.0',
    install_requires=install_requires,
    description='A Library to fill and flatten pdfs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Tyler Houssian',
    author_email="tylerhoussian@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    url='https://github.com/t-houssian/fillpdf',
)