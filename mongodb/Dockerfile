FROM centos

RUN yum update -y
RUN yum install -y  wget
WORKDIR /tmp
RUN  wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-9.noarch.rpm  
RUN rpm -ivh epel-release-7-9.noarch.rpm
RUN yum install -y mongodb
RUN yum install -y mongodb-server

WORKDIR /data

EXPOSE 27017

CMD ["mongod","--dbpath","/data"]
