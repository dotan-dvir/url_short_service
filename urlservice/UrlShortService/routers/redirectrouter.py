import falcon.request
import falcon.response
import re
import json

from util.stringutil import validateString
from util.httputil import sendErrorMessage,sendSuccessMessage,sendSuccessObject,sendRedirectResponse
from .baserouter import BaseRouter

class RedirectRouter(BaseRouter):

    def __init__(self,userHandler,urlsHandler,urlsHistoryHandler):
        super().__init__(userHandler,urlsHandler,urlsHistoryHandler)


    def on_get(self,request,response,shortform):
        '''
        Redirect the user to the URL and add a visit to the history. Replly with 404 if the parameters are not correct
        or no such short form was found
        :param request: falcon http request object
        :param response: falcon http reply object
        :param shortform: the short form part of the URL
        :return: void
        '''
        if(validateString(shortform) == False):
            sendErrorMessage(response,falcon.HTTP_404,"Not found")
            return

        status, urlLongForm = self.urlsHandler.retrieveURLLongForm(shortform)

        if(status == False):
            sendErrorMessage(response,falcon.HTTP_404,"Not found")
            return

        self.urlsHistoryHandler.insertURLVisit(shortform)

        sendRedirectResponse(response,urlLongForm)



