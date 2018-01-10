#!/bin/bash

# install Dash and requirements for the app in a virtual env

# module unload python
# module load python/2.7.3
unset PYTHONPATH

virtualenv venv --no-site-packages
source venv/bin/activate

pip install -r requirements.txt
pip install plotly --upgrade
