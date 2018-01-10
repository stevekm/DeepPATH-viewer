SHELL:=/bin/bash

none:

# build the Docker container
build:
	/bin/cp ../requirements.txt . && docker build -t stevekm/deeppath-viewer .

# run the Docker container to start a Jupyter Notebook
run:
	docker run --rm -it -p 8888:8888 -v "${PWD}:/home/jovyan" stevekm/deeppath-viewer
