# container for Jupyter Notebook to test new features to add to the web app
# https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook
FROM jupyter/datascience-notebook

MAINTAINER Stephen M. Kelly

# update Python packages with the req's for this repo
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN pip install plotly --upgrade
