FROM ubuntu:18.04
MAINTAINER  nunomsilvanunes@gmail.com
MAINTAINER  ammar257ammar@gmail.com

RUN apt-get update

RUN apt-get -y install git
RUN apt-get -y install python3-pip

RUN apt-get install telnet

RUN mkdir /scholia/
WORKDIR /scholia/


RUN git clone -b ext-sparql https://github.com/ammar257ammar/scholia.git . 
RUN chmod +x startScholia.sh

RUN pip3 install -r requirements.txt

EXPOSE 8100

ENTRYPOINT ["./startScholia.sh"]