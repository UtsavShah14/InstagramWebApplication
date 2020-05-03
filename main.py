import os
import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import images

from myuser import MyUser
from post import Post
from uploadhandler import UploadHandler
from user_profile import UserProfile
from list import List
from comments import Comments

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'], autoescape = True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user() #Fetching the current user

        #If user is not loogged in, display main_guest page
        if user == None:

            template_values = {
                'url':users.create_login_url(self.request.uri),
            }

            template = JINJA_ENVIRONMENT.get_template('main_guest.html')
            self.response.write(template.render(template_values))
            return

        #If user is logged in
        #We fetch the user key and details
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        #If this is a new user, we create a datastore entity for it
        if myuser == None:
            email_address = user.email().lower()
            name = user.email().split('@')
            myuser = MyUser(id=user.user_id(), email_address=email_address, username = name[0].lower(), followers_count = 0, following_count = 0)
            myuser.put()

        img_url_list = []
        no_posts = False

        if myuser.following != []:
            query = Post.query().filter(ndb.OR(Post.post_by.IN(myuser.following),Post.post_by==myuser_key)).order(-Post.upload_time).fetch(50)
        else:
            query = Post.query().filter(Post.post_by==myuser_key).order(-Post.upload_time).fetch(50)

        if query != []:
            for i in query:
                url = images.get_serving_url(i.uploads)
                img_url_list.append(url)
        else:
            no_posts = True

        #With the details, we render the Home page of our application
        template_values = {
            'url':users.create_logout_url(self.request.uri),
            'user':user,
            'myuser': myuser,
            'img_url_list': img_url_list,
            'query': query,
            'no_posts': no_posts,
            'upload_url' : blobstore.create_upload_url('/upload')
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):

        user = users.get_current_user()

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        comment = self.request.get('comment')
        post_id = self.request.get('query')
        post_key = ndb.Key(Post, long(post_id))
        post = post_key.get()
        new_comment = Comments(comment = comment, comment_by = myuser_key)
        post.comments.append(new_comment)
        post.put()
        self.redirect('/')


app = webapp2.WSGIApplication([
        ('/',MainPage),
        ('/upload', UploadHandler),
        ('/user_profile', UserProfile),
        ('/list', List)
        ], debug = True)
