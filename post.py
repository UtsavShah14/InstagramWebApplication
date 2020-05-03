from google.appengine.ext import ndb
from comments import Comments

class Post(ndb.Model):
    image_name = ndb.StringProperty()
    uploads = ndb.BlobKeyProperty()
    caption = ndb.StringProperty()
    upload_time = ndb.DateTimeProperty(auto_now_add = True)
    post_by = ndb.KeyProperty()
    comments = ndb.StructuredProperty(Comments, repeated = True)
