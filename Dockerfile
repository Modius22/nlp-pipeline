FROM ubuntu:16.04
#MAINTANER Your Name "christian.piazzi@gmx.de"

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt
RUN python3 -m nltk.downloader stopwords
RUN mkdir working
COPY ./src /app/src
WORKDIR /app/src
ENTRYPOINT ["python"]
CMD [ "api.py" ]