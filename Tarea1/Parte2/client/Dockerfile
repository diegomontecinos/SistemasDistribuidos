FROM ubuntu

RUN apt-get update && \
	apt-get -y install sudo 

RUN sudo apt-get -y install python3-pip

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

CMD []