from google.appengine.ext import ndb

class Post(ndb.Model):
    image_name = ndb.StringProperty()
    uploads = ndb.BlobKeyProperty()
    caption = ndb.StringProperty()
    upload_time = ndb.DateTimeProperty(auto_now_add = True)
    post_by = ndb.KeyProperty()
    comments = ndb.StructuredPropetry(Comments, repeated = True)

class Comments(ndb.Model):
    comment = ndb.StringProperty()
    comment_by = ndb.KeyProperty()
    comment_time = ndb.DateTimeProperty(auto_now_add = True)
