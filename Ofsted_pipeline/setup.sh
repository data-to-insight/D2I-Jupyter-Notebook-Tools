#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Install additional system-level dependencies/packages
sudo apt-get update                                         # requ' to run the below
pip install openpyxl                                        # create repo tree reference file in xls
pip install tabulate                                        # create change log table formatting
pip install textblob
pip install gensim
pip install nltk

# Install the Python extension for Visual Studio Code
code --install-extension ms-python.python --force