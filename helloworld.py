import webapp2

class MainPage(webapp2.RequestHandler):

    def get(self):

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.request.path)
        self.response.write('\n')
        self.response.write(str(self.request.GET))
        self.response.write('\n')

application = webapp2.WSGIApplication([
    webapp2.Route(r'/.*', handler=MainPage, name='main'),
], debug=True)
