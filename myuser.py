from google.appengine.ext import ndb
from post import Post

class MyUser(ndb.Model):
    username = ndb.StringProperty()
    email_address = ndb.StringProperty()
    followers = ndb.KeyProperty(repeated = True)
    followers_count = ndb.IntegerProperty()
    following = ndb.KeyProperty(repeated = True)
    following_count = ndb.IntegerProperty()
    posts = ndb.KeyProperty(repeated = True)
