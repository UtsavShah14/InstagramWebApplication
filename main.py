import os
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
JINJA_ENVIRONMMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'], autoescape = True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = ''
        user = users.get_current_user()

        if user == None:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

            template_values = {
                'url':url,
                'url_string':url_string,
                'user':user
            }

            template = JINJA_ENVIRONMMENT.get_template('main_guest.html')
            self.response.write(template.render(template_values))
            return

        url = users.create_logout_url(self.request.uri)
        url_string = 'logout'

        # The myuser_key variable is the KEY that will delete the eniter row
        # myuser_key is what fetches the key value, user.id() is what gives the id
        myuser_key = ndb.Key('MyUser', user.user_id())

        # The myuser variable is the variable that will be used to edit the variable
        # myuser will be used to edit values
        myuser = myuser_key.get()

        if myuser == None:
            email_address = user.email()
            name = user.email().split('@')
            myuser = MyUser(id=user.user_id(),email_address=email_address, username = name[0], posts = [])
            #The value returned by this statement is same as the value returend by myuser_key
            myuser.put()

        template_values = {
            'url':url,
            'url_string':url_string,
            'user':user,
            'myuser': myuser
        }

        template = JINJA_ENVIRONMMENT.get_template('main.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/',MainPage)], debug = True)
