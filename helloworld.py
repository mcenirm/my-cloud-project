from google.appengine.api import users

import webapp2


class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Hello, ' + user.nickname())
            if users.is_current_user_admin():
                self.response.write(' (admin)')
            self.response.write('\n')
            self.response.write('\n')
            self.response.write(str(user))
            self.response.write('\n')
            self.response.write('auth_domain    '+str(user.auth_domain())+'\n')
            self.response.write('email    '+str(user.email())+'\n')
            self.response.write('federated_identity    '+str(user.federated_identity())+'\n')
            self.response.write('federated_provider    '+str(user.federated_provider())+'\n')
            self.response.write('nickname    '+str(user.nickname())+'\n')
            self.response.write('user_id    '+str(user.user_id())+'\n')

        else:
            self.redirect(users.create_login_url(self.request.uri))


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

