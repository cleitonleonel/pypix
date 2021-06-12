from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pypix",
    version="1.0.3",
    include_package_data=True,
    author="Cleiton Leonel Creton",
    author_email="cleiton.leonel@gmail.com",
    description="Facilitates the generation of dynamic and static br-codes for transactions via PIX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cleitonleonel/pypix.git",
    packages=["pypix"],
    install_requires=[
        'Pillow',
        'qrcode',
        'crc16',
        'Pillow',
        'amzqr'
    ],
    project_urls={
        "Bug Tracker": "https://github.com/cleitonleonel/pypix/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
