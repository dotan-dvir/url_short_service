from pymongo import MongoClient
import time

from util.stringutil import validateString
from .basehandler import BaseHandler
import logging

class UrlsHistoryHandler(BaseHandler):
    def __init__(self,dbURL,dbName):
        '''
        Initialize the user handler object with a reference to the DB URL and the DB name
        :param dbURL: the URL to the momgo db deployment
        :param dbName: the name of the database to use
        '''
        super().__init__(dbURL,dbName,"urlshistory")
        self._log = logging.getLogger()



    def countUrlVisits(self,urlShortForm):
        '''
        Count the number of visits for a given URL
        :param urlShortForm:
        :return: a booleam indicarting success or failure and an integer indicating the number of visits or -1
        in case of failure
        '''

        results = -1

        if (super().isConnected() == False):
            return False,results

        if (validateString(urlShortForm)==False):
            return False,results

        try:
            results = self.dbCollection.count({"shortform":urlShortForm})
        except:
            results = -1
            return False, results

        return True, results




    def insertURLVisit(self,urlShortForm):
        '''
        Insert a visit to the database
        :param urlShortForm:
        :return: True on success and False otherwise
        '''

        if(super().isConnected() == False):
            return False

        if(validateString(urlShortForm)== False):
            return False


        insertId = None

        try:
            insertId = self.dbCollection.insert_one({"shortform":urlShortForm,"epochtime":int(time.time())})
        except:
            insertId = None

        if(insertId == None):
            return False

        return True

    def getVisitsForURL(self,urlShortForm):
        '''
        Get all the visits for a specified URL
        :param urlShortForm: the short form of the URL
        :return: A tuple of boolean and an array containong the visits for the URL
        '''
        visitsForUrl = []

        if(super().isConnected()==False):
            return False,visitsForUrl


        print(urlShortForm)

        if(validateString(urlShortForm)== False):
            return False,[]


        # Remove ObjectId from the results because it is not serializable and convert the epoch time to human readable date times
        # in UTC time zone
        try:
            for urlVisit in self.dbCollection.find({"shortform":urlShortForm}):
                visitsForUrl.append({"visitdatetime":time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(urlVisit["epochtime"]))})
        except:
            visitsForUrl = []
            return False,visitsForUrl


        return True,visitsForUrl


if __name__ == "__main__":
    pass
