FROM continuumio/miniconda3

MAINTAINER Your Name Here


RUN mkdir /apps ; mkdir /apps/dev ;  mkdir /apps/dev/maestro ; mkdir /logs
COPY . /apps/prod/maestro

# update and configure conda and pip
RUN conda config --set ssl_verify false
RUN python -m pip install --upgrade --trusted-host pypi.org pip

WORKDIR /apps/dev/maestro

#ENV FLASK_PORT=5000
#ENV JUPYTER_PORT=8888
#EXPOSE $FLASK_PORT $JUPYTER_PORT

# make sure we're up to date each time we run the container
#ENTRYPOINT ["python","/apps/prod/maestro/core/core_functionality.py"]
#CMD ["/bin/bash"]

#### build command
## docker build -f Dockerfile -t yourname/maestro .
