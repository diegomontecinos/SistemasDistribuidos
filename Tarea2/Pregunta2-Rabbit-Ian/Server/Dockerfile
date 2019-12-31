FROM ubuntu

RUN apt-get update && \
	apt-get -y install sudo 

RUN sudo apt-get -y install python3-pip
RUN sudo apt-get -y install vim

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r /requirements.txt
CMD []