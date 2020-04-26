from google.appengine.ext import ndb

class Post(ndb.Model):
    # uploads =
    # caption =
    # comments =
    upload_time = ndb.DateTimeProperty(auto_now_add = True)
