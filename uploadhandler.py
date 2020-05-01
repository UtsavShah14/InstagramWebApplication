from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from google.appengine.api import users
from post import Post

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        upload = self.get_uploads()[0]
        blobinfo = blobstore.BlobInfo(upload.key())
        image_name = blobinfo.filename

        collection_key = ndb.Key('Post', None)

        collection = Post(image_name=image_name, uploads=upload.key(), caption = self.request.get('caption'), post_by = myuser_key)
        post_key = collection.put()
        myuser.posts.append(post_key)
        myuser.put()
        self.redirect('/')
