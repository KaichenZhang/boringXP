FROM ubuntu:latest
MAINTAINER Kaichen Zhang "ac1102919258@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev
COPY . /app
WORKDIR /app
RUN pip install -r packages.txt
ENTRYPOINT ["python"]
EXPOSE 5005
CMD ["server.py"]