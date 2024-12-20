# See https://opendrift.github.io for usage

FROM condaforge/mambaforge:23.11.0-0

ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /code
WORKDIR /code

# Install opendrift environment into base conda environment
COPY environment.yml .
RUN mamba env update -n base -f environment.yml

# Install opendrift
ADD . /code
RUN pip install -e .
