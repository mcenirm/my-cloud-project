import webapp2

#########################################################################################

class FacebookHandler(webapp2.RequestHandler):

    def get(self, id):
        feed_url = 'https://www.facebook.com/feeds/page.php?id=' + id + '&format=RSS20'
        return redirect(feed_url, permanent=True)

#########################################################################################

application = webapp2.WSGIApplication([
    webapp2.Route('/facebook/<id:\d+>', handler=FacebookHandler),
], debug=True)
