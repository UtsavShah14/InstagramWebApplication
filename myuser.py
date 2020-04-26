from google.appengine.ext import ndb
from post import Post

class MyUser(ndb.Model):
    username = ndb.StringProperty()
    email_address = ndb.StringProperty()
    followers = ndb.KeyProperty(repeated = True)
    following = ndb.KeyProperty(repeated = True)
    posts = ndb.KeyProperty(Post, repeated = True)
