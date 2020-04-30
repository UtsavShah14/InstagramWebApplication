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

class UserProfile(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        if user == None:
            template_values = {
                'url':users.create_login_url(self.request.uri),
            }

            template = JINJA_ENVIRONMENT.get_template('main_guest.html')
            self.response.write(template.render(template_values))
            self.redirect('/')
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        query = Post.query().filter(Post.post_by == user.email()).order(-Post.upload_time).fetch()

        img_url_list = []
        for i in query:
            # if img_url_list == None:
            #     url = img_url_list.insert([images.get_serving_url(i.get().uploads)])
            # else:
            url = images.get_serving_url(i.uploads)
            img_url_list.append(url)
        # self.response.write(url_list)

        # post_img_key = ndb.Key('Post')
        # post_img = post_img_key.get()
        # img_url_list = Post.query().filter(Post.post_by==myuser.email_address).fetch()

        template_values = {
            'url':users.create_logout_url(self.request.uri),
            # 'url_string':'logout',
            'user':user,
            'myuser': myuser,
            'img_url_list': img_url_list,
            # 'collection_key':collection_key,
            # 'collection': collection
            'upload_url' : blobstore.create_upload_url('/upload'),
        }

        template = JINJA_ENVIRONMENT.get_template('user_profile.html')
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
