FROM ubuntu:22.04

RUN apt-get update && apt-get install -y openjdk-17-jdk

WORKDIR /home/app

COPY Hello.java .

RUN javac Hello.java

CMD ["java", "Hello"]
