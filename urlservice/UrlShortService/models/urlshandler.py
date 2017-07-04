from pymongo import MongoClient
from datetime import datetime

from util.stringutil import validateString
from .basehandler import BaseHandler

import logging

class UrlsHandler(BaseHandler):
    '''
    A class for handling URL objects in the service - it implements the logic or adding the URLs into the Mongo database
    instance and reading the full URL on a redirect request
    '''

    def __init__(self,dbURL,dbName):
        '''
        The constructor
        :param dbURL: the URL (mongofb://host:port) of the mongo instance
        :param dbName: the name of the database to use
        '''
        super().__init__(dbURL,dbName,"urls")


    def insertURL(self,userName,urlLongForm,urlShortForm):
        '''
        Insert a URL into the database
        :param userName: the username generating the URL
        :param urlLongForm:  the long form of the URL
        :param urlShortForm:  the desired short form
        :return:  a tuple of boolean indicating success and string giving an error message or status
        '''

        if(super().isConnected() == False):
            return False,"Internal server error"

        if(validateString(userName)==False or validateString(urlLongForm) == False or validateString(urlShortForm) == False):
            return False,"The parameters cannot be empty"

        # Look if the database already contains a URL with the short form
        if(self.dbCollection.find_one({"shortform": urlShortForm}) != None):
            return False, "Short form already exists in the databsae. Try another short form."

        objectId = None

        # Short form does not exist - insert into the database
        try:
            objectId = self.dbCollection.insert_one({"username":userName,"longform":urlLongForm,"shortform":urlShortForm,"createtime":str(datetime.now())})
        except:
            objectId = None

        if(objectId == None):
            return False, "Failed to commit changes to the database"
        else:
            return True,"Change committed succesfully. Url short path is "+urlShortForm

    def retrieveURLLongForm(self,shortForm):
        '''
        Returns a tuple of boolean indicating success and a URL to redirect to if found
        :param shortForm: the short form of the URL
        :return:
        '''
        if(super().isConnected() == False):
            return False,"Internal server error"

        if(validateString(shortForm)==False):
            return False,"Cannot redirect from empty values"

        result = None

        try:
            result = self.dbCollection.find_one({"shortform":shortForm})
        except:
            result = None

        if(result == None):
            return False,"URL not found"

        return True, result["longform"]


    def retrieveURLsForUser(self,userName):
        '''
        Return the URLs in short form for the user id provided
        :param userName: the user id to provide the URLs for
        :return: a tuple of boolean and array containing the success of the operation and the urls for the user if successful
        '''

        if(super().isConnected() == False):
            return False,"Internal server errror"

        urlsForUser = []

        if(validateString(userName)==False):
            return False,urlsForUser

        # Removing the ObjectId field from the results as they are not serializable to JSON
        try:
            for url in self.dbCollection.find({"username": userName}):
                urlsForUser.append({"url":url["longform"],"shortform":url["shortform"],"createtime":url["createtime"]})
        except:
            urlsForUser = []
            return False,urlsForUser


        return True,urlsForUser

    def retrieveURLForUser(self,userName,shortForm):
        if (super().isConnected() == False):
            return False, "Internal server errror"

        result = None

        if (validateString(userName) == False):
            return False, result


        try:
            result = self.dbCollection.find_one({"username":userName,"shortform":shortForm})
        except:
            result = None

        if(result == None):
            return False, result

        return True,result


if __name__ == "__main__":
    pass