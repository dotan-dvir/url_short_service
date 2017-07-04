import falcon.request
import falcon.response
import falcon

from util.stringutil import validateString

class BaseRouter(object):
    '''
    A class for implementing base router functionality
    '''

    def __init__(self,userHandler,urlsHandler,urlsHistoryHandler):
        self.usersHandler = userHandler
        self.urlsHandler = urlsHandler
        self.urlsHistoryHandler = urlsHistoryHandler


    def authenticateUser(self,request,response):
        # Reterieve the values for the username and password from the headers


        userName = request.get_header("username", False, "")
        password = request.get_header("password", False, "")


        if (validateString(userName) == False or validateString(password) == False):
            return False,falcon.HTTP_400, "User parameters are missing or wrong"

        status,message = self.usersHandler.authenticateUser(userName, password)

        if(status == False):
            return False,falcon.HTTP_403,"Could not authenticate user."

        return True,falcon.HTTP_200,"User authenticated successfully"

