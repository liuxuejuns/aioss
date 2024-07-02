FROM centos/python-36-centos7:latest
USER root                      
LABEL maintainer aoiss                
ENV PYTHONUNBUFFERED 1                 
WORKDIR /aoiss/aoiss
COPY requirements.txt /aoiss/aoiss/         
RUN pip install -r requirements.txt
RUN yum install -y cifs-utils && yum clean all