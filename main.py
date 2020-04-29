import os
import webapp2
import jinja2
import uuid

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import images

from myuser import MyUser
from post import Post
from uploadhandler import UploadHandler
# from downloadhandler import DownloadHandler

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'], autoescape = True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        if user == None:
            # url = users.create_login_url(self.request.uri)
            # url_string = 'login'

            template_values = {
                'url':users.create_login_url(self.request.uri),
                # 'url_string':'login',
                # 'user':user
            }

            template = JINJA_ENVIRONMENT.get_template('main_guest.html')
            self.response.write(template.render(template_values))
            return

        # url = users.create_logout_url(self.request.uri)
        # url_string = 'logout'

        # The myuser_key variable is the KEY that will delete the eniter row
        # myuser_key is what fetches the key value, user.id() is what gives the id
        myuser_key = ndb.Key('MyUser', user.user_id())

        # The myuser variable is the variable that will be used to edit the variable
        # myuser will be used to edit values
        myuser = myuser_key.get()

        # id = uuid.uuid4()
        # # collection_key=''
        # # collection=''
        # collection_key = ndb.Key('Post', id)
        # collection = collection_key.get()
        # if collection == None:
        #     collection = Post(id=id)
        #     collection.put()

        if myuser == None:
            email_address = user.email()
            name = user.email().split('@')
            myuser = MyUser(id=user.user_id(),email_address=email_address, username = name[0])
            #The value returned by this statement is same as the value returend by myuser_key
            myuser.put()

        template_values = {
            'url':users.create_logout_url(self.request.uri),
            # 'url_string':'logout',
            'user':user,
            'myuser': myuser,
            # 'collection_key':collection_key,
            # 'collection': collection
            'upload_url' : blobstore.create_upload_url('/upload'),
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    # def post(self):
    #     self.response.headers['Content-Type'] = 'text/html'
    #     user = users.get_current_user()
    #     self.request.get('button')
    #     collection_key = ndb.Key('Post', 'users.get_current_user()')
    #     collection = collection_key.get()
    #
    #     if collection == None:
    #         collection = Post(id=user.user_id())
    #         collection.put()
    #
    #     template_values = {
    #         'collection' : collection,
    #         'upload_url' : blobstore.create_upload_url('/upload'),
    #         }
    #
    #     template = JINJA_ENVIRONMENT.get_template('main.html')
    #     self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
        ('/',MainPage),
        ('/upload', UploadHandler),
        # ('/downlaod', DownloadHandler)
        ], debug = True)
