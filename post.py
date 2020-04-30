from google.appengine.ext import ndb

class Post(ndb.Model):
    image_name = ndb.StringProperty()
    uploads = ndb.BlobKeyProperty()
    caption = ndb.StringProperty()
    upload_time = ndb.DateTimeProperty(auto_now_add = True)
    post_by = ndb.StringProperty()
    # comments = ndb.textPropetry()
    # image_url = ndb.StringProperty(repeated=True)
