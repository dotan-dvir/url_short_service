from models.userhandler import UserHandler
import json
import re
import falcon.request
import falcon.response

from util.stringutil import validateString
from util.httputil import sendErrorMessage,sendSuccessMessage,sendSuccessObject,sendRedirectResponse
from .baserouter import BaseRouter

class AddUserRouter(BaseRouter):
    def __init__(self,userHandler,urlsHandler,urlsHistoryHandler):
        super().__init__(userHandler,urlsHandler,urlsHistoryHandler)

    def on_post(self,request,response):
        '''
        Create a new user using the user service
        :param request: the HTTP request parameter
        :param response: the HTTP response parameter
        :return: void
        '''

        data = None
        if(request.content_length):
            data = json.load(request.stream)

        if(data == None):
            return sendErrorMessage(response,falcon.HTTP_400," No parameters sent to method")


        userName = data["username"]
        password = data["password"]


        if(validateString(userName)== False or validateString(password) == False):
            sendErrorMessage(response,falcon.HTTP_400,"Bad parameters sent to method")
            return


        status,message = self.usersHandler.addUser(userName,password)

        if(status == False):
            sendErrorMessage(response,falcon.HTTP_400,message)
        else:
            sendSuccessMessage(response,falcon.HTTP_200,message)
