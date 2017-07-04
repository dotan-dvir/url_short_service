'''
The main file for the URL shortener service - implemented using the Falcon REST framework for Python
'''


# External imports
import falcon
import os


# Internal imports
from models.userhandler import UserHandler
from models.urlshandler import UrlsHandler
from models.urlshistoryhandler import UrlsHistoryHandler
from routers.adduserrouter import AddUserRouter
from routers.urlsrouter import UrlsRouter
from routers.redirectrouter import RedirectRouter
from routers.urlinforouter import UrlInfoRouter




# Retrieve some OS variables
mongodb_location = os.environ.get("DBURL","mongodb://localhost:27017/")
mongodb_name = os.environ.get("DBNAME","urlsdb")
memcached_location = os.environ.get("MEMCACHEHOST","localhost")

# Create DB Handlers and connect to the database
usersHandler = UserHandler(mongodb_location,mongodb_name)
usersHandler.connectToDatabase()
urlsHandler = UrlsHandler(mongodb_location,mongodb_name,memcached_location)
urlsHandler.connectToDatabase()
urlsHistoryHandler = UrlsHistoryHandler(mongodb_location,mongodb_name)
urlsHistoryHandler.connectToDatabase()


# Create routers
addUsersRouter = AddUserRouter(usersHandler,urlsHandler,urlsHistoryHandler)
urlsRouter = UrlsRouter(usersHandler,urlsHandler,urlsHistoryHandler)
redirectRouter = RedirectRouter(usersHandler,urlsHandler,urlsHistoryHandler)
urlInfoRouter = UrlInfoRouter(usersHandler,urlsHandler,urlsHistoryHandler)


# Configure the REST framework routing
app = falcon.API()
app.add_route("/users",addUsersRouter)
app.add_route("/urls",urlsRouter)
app.add_route("/{shortform}",redirectRouter)
app.add_route("/urls/{shortform}",urlInfoRouter)
