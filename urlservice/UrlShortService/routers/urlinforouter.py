import falcon.request
import falcon.response
import json
import re

from util.stringutil import validateString
from util.httputil import sendErrorMessage,sendSuccessMessage,sendSuccessObject,sendRedirectResponse
from .baserouter import BaseRouter


class UrlInfoRouter(BaseRouter):

    def __init__(self,userHandler,urlsHandler,urlsHistoryHandler):
        super().__init__(userHandler,urlsHandler,urlsHistoryHandler)


    def on_get(self,request,response,shortform):
        status,errorCode,message = super().authenticateUser(request,response)

        if(status == False):
            sendErrorMessage(response,errorCode,message)
            return

        userName = request.get_header("username",False,"")

        if(userName == None):
            sendErrorMessage(response,falcon.HTTP_500,"Internal server error")

        status,urlInfo = self.urlsHandler.retrieveURLForUser(userName,shortform)

        if(status == False):
            sendErrorMessage(response,falcon.HTTP_404,"Short form URL not found: "+shortform)
            return

        status,urlVisits = self.urlsHistoryHandler.countUrlVisits(shortform)

        if(status == False):
            sendErrorMessage(response,falcon.HTTP_500,"Internal server error")
            return


        results = {}
        results["url"] = urlInfo["longform"]
        results["shortform"] = shortform
        results["visits"] = urlVisits

        sendSuccessObject(response,falcon.HTTP_200,results)





