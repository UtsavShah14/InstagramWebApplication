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

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'], autoescape = True)

class List(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user() #Fetching the current user

        #If user is not loogged in, display main_guest page
        if user == None:
            self.redirect('/')
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        user_id = self.request.get('id')
        profile_key = ndb.Key('MyUser', user_id)
        profile = profile_key.get()

        request = self.request.get('request')

        template_values = {
            'url':users.create_logout_url(self.request.uri),
            'user':user,
            'myuser': myuser,
            'profile': profile,
            'request': request,
            'upload_url' : blobstore.create_upload_url('/upload'),
        }

        template = JINJA_ENVIRONMENT.get_template('list.html')
        self.response.write(template.render(template_values))

    def post(self):

        user = users.get_current_user()

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        # user_id = self.request.get('id')
        # profile_key = ndb.Key('MyUser', user_id)
        # profile = profile_key.get()

        if self.request.get('button') == 'search':
            search_result = []
            search_string = self.request.get('search_string').lower()
            user_list = MyUser.query().order(MyUser.username).fetch()
            for i in user_list:
                temp = i.username.startswith(search_string)
                if temp:
                    search_result.append(i)

            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            template_values = {
                'url':users.create_logout_url(self.request.uri),
                'user':user,
                'myuser': myuser,
                'upload_url' : blobstore.create_upload_url('/upload'),
                'search_result': search_result
            }

            template = JINJA_ENVIRONMENT.get_template('list.html')
            self.response.write(template.render(template_values))
