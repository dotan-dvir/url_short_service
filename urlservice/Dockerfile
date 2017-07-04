FROM python:3.6.0
RUN pip install pymongo
RUN pip install pymemcache
RUN pip install falcon
RUN pip install waitress
ENV DBURL mongodb://mongodb:27017
ENV DBNAME urlsdb
ENV MEMCACHEHOST memcached
WORKDIR /usr/local/bin/UrlShortService
EXPOSE 8080
CMD ["waitress-serve","--port","8080","app:app"]

 
