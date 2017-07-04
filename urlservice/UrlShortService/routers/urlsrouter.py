import falcon.request
import falcon.response
import re
import json
import hashlib

from models.userhandler import UserHandler
from models.urlshandler import UrlsHandler

from util.stringutil import validateString
from util.httputil import sendErrorMessage,sendSuccessMessage,sendSuccessObject,sendRedirectResponse
from .baserouter import BaseRouter


class UrlsRouter(BaseRouter):

    '''
    A class implementing the get and post methods for the URLs API
    '''

    def __init__(self,usersHandler,urlsHandler,urlsHistoryHandler):
        '''
        Init the class with the correct handlers
        :param usersHandler: handles users requests
        :param urlsHandler:  handles url requests
        '''
        super().__init__(usersHandler,urlsHandler,urlsHistoryHandler)

    def on_get(self,request,response):
        '''
        List all the users for a particular user
        The user is authenticated using two headers : username and password
        :param request: the falcon HTTP request object
        :param response: the falcon HTTP response object
        :return: void
        '''

        # Reterieve the values for the username and password from the headers

        status,errorCode,message = super().authenticateUser(request,response)

        if(status== False):
            sendErrorMessage(response,errorCode,message)
            return

        userName = request.get_header("username",False,"")

        status,urls = self.urlsHandler.retrieveURLsForUser(userName)

        if(status == False):
            sendErrorMessage(response,falcon.HTTP_500,"Internal server errror")
            return

        for url in urls:
            status,visits = self.urlsHistoryHandler.countUrlVisits(url["shortform"])

            if(status == False):
                sendErrorMessage(response,falcon.HTTP_500,"Internal server error")
                return
            url["visits_count"] = visits

        sendSuccessObject(response,falcon.HTTP_200,urls)

    def on_post(self,request,response):
        # Reterieve the values for the username and password from the headers
        status,errorCode,message = super().authenticateUser(request,response)

        if(status == False):
            sendErrorMessage(response,errorCode,message)
            return

        userName = request.get_header("username","False","")

        # Retrieve the post data
        data = None

        if(request.content_length):
            data = json.load(request.stream)

        if(data == None):
            sendErrorMessage(response,falcon.HTTP_400,"Bad parameters provided")

        # Extract the data from the post

        urlLongForm = None
        urlShortForm = None

        try:
            urlLongForm = data["longform"]
        except:
            pass

        if(validateString(urlLongForm)== False):
            sendErrorMessage(response,falcon.HTTP_400,"The parameter longform is missing in the message")
            return

        try:
            urlShortForm = data["shortform"]
        except:
            urlShortForm = hashlib.sha256((urlLongForm+userName).encode('utf-8')).hexdigest()[0:8]

        if(validateString(urlShortForm)==False):
            sendErrorMessage(response,falcon.HTTP_400,"The parameter shortform is not correct")
            return

        status, message = self.urlsHandler.insertURL(userName, urlLongForm, urlShortForm)

        if (status == False):
            sendErrorMessage(response, falcon.HTTP_400, message)
            return

        sendSuccessMessage(response, falcon.HTTP_200, message)

