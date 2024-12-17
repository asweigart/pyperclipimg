import io
import os
import re
from setuptools import setup, find_packages

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

# Find version info from module (without importing the module):
init_filename = "src/pyperclipimg/__init__.py"
with open(init_filename, "r") as fileObj:
    mo = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fileObj.read(), re.MULTILINE
    )

    if mo is not None:
        version = mo.group(1)
    else:
        raise Exception('__version__ variable not found in ' + init_filename)

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fileObj:
    long_description = fileObj.read()

setup(
    name="pyperclipimg",
    version=version,
    url="https://github.com/asweigart/pyperclipimg",
    author="Al Sweigart",
    author_email="al@inventwithpython.com",
    description=("""Cross-platform copy() and paste() Python functions for images."""),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    test_suite="tests",
    install_requires=['pillow>=9.4.0;platform_system=="Linux"',
                      'pillow>=1.1.4;platform_system=="Windows"',
                      'pillow>=3.3.0;platform_system=="Darwin"',
                      'pyobjc-framework-quartz;platform_system=="Darwin"',
                      'pywin32;platform_system=="Windows"',
                      ],
    keywords="",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
