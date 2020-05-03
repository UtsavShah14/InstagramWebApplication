from google.appengine.ext import ndb

class Comments(ndb.Model):
    comment = ndb.StringProperty()
    comment_by = ndb.KeyProperty()
    comment_time = ndb.DateTimeProperty(auto_now_add = True)
