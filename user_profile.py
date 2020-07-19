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
            self.redirect('/')
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        #id, key of the user whos' rprofile is to be displayed
        user_id = self.request.get('id')
        profile_key = ndb.Key('MyUser', user_id)
        profile = profile_key.get()

        #query for user uploads
        image_list = Post.query().filter(Post.post_by == profile_key).order(-Post.upload_time).fetch()

        #creating urls for the user uploads
        img_url_list = []
        for i in image_list:
            url = images.get_serving_url(i.uploads)
            img_url_list.append(url)

        template_values = {
            'url':users.create_logout_url(self.request.uri),
            'user':user,
            'myuser': myuser,
            'profile': profile,
            'img_url_list': img_url_list,
            'upload_url' : blobstore.create_upload_url('/upload'),
        }

        template = JINJA_ENVIRONMENT.get_template('user_profile.html')
        self.response.write(template.render(template_values))

    def post(self):

        user = users.get_current_user()

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        user_id = self.request.get('id')
        profile_key = ndb.Key('MyUser', user_id)
        profile = profile_key.get()

        button = self.request.get('button')

        if button == 'Follow' or button == 'Follow Back':
            status = 'Followed'
            followers_count = profile.followers_count + 1
            following_count = myuser.following_count + 1
            profile.followers_count = followers_count
            myuser.following_count = following_count
            profile.followers.append(myuser_key)
            myuser.following.append(profile_key)
            myuser.put()
            profile.put()

        if button == 'UnFollow':
            status = 'Unfollowed'
            followers_count = profile.followers_count - 1
            following_count = myuser.following_count - 1
            profile.followers_count = followers_count
            myuser.following_count = following_count
            profile.followers.remove(myuser_key)
            myuser.following.remove(profile_key)
            myuser.put()
            profile.put()

        image_list = Post.query().filter(Post.post_by == profile_key).order(-Post.upload_time).fetch()

        img_url_list = []
        for i in image_list:
            url = images.get_serving_url(i.uploads)
            img_url_list.append(url)

        template_values = {
            'url':users.create_logout_url(self.request.uri),
            'user':user,
            'myuser': myuser,
            'profile': profile,
            'img_url_list': img_url_list,
            'status': status,
            'upload_url' : blobstore.create_upload_url('/upload'),
        }

        template = JINJA_ENVIRONMENT.get_template('user_profile.html')
        self.response.write(template.render(template_values))
