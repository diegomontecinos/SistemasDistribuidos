FROM ubuntu


# Install Erlang + Rabbitmq
# Install the erlang downloader
RUN apt-get update && \
	apt-get -y install sudo

RUN sudo apt-get install wget curl gnupg -y

RUN curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc | sudo apt-key add -
RUN sudo apt-get -y install apt-transport-https 
RUN sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list
RUN sudo apt-get update -y
RUN sudo apt-get install rabbitmq-server -y --fix-missing

RUN sudo apt-get -y install python3-pip
RUN sudo apt-get -y install vim

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r /requirements.txt
CMD []