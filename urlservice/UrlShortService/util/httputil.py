'''
A file containing some common http functions
'''
import json
import falcon.request
import falcon.response


def sendErrorMessage(response, responseCode, errorMessage):
    response.status = responseCode
    response.body = json.dumps({"message":errorMessage})


def sendSuccessMessage(response, responseCode, message):
    response.status = responseCode
    response.body = json.dumps({"message":message})

def sendSuccessObject(response,responseCode,object):
    response.status = responseCode
    response.body = json.dumps(object,sort_keys=True,indent=4, separators=(',', ': '))

def sendRedirectResponse(response,redirectLocation):
    response.content_type= "text/html"
    response.status=falcon.HTTP_302
    response.set_header("Location",redirectLocation)
