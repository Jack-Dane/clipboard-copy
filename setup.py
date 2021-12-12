
from setuptools import setup
import os
import platform

if platform.system() == "Linux":
    os.system("sudo apt-get install xclip")

setup(
    name="Clipboard Copier",
    version="1.0",
    description="Clipboard Copier Storage",
    author="Jack Dane",
    author_email="jackdane@jackdane.co.uk",
    url="https://www.jackdane.co.uk",
    install_requires=["keyboard", "pyperclip"]
)
