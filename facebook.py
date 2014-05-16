import webapp2
import urllib2
import json
from django.utils import feedgenerator, dateparse
from html2text import html2text

#########################################################################################

class FacebookHandler(webapp2.RequestHandler):

    def get(self, id):

        feed_url = 'https://www.facebook.com/feeds/page.php?id=' + id + '&format=json'
        feed_file = 'facebook.' + id + '.json'

        self.response.headers['Last-Modified'] = 'Wed, 14 May 2014 11:16:06 -0700'
        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.headers['Pragma'] = 'no-cache'
        self.response.headers['Cache-Control'] = 'private, no-cache, no-store, must-revalidate'
        self.response.headers['Expires'] = 'Sat, 01 Jan 2000 00:00:00 GMT'

        feed_in = json.load(open(feed_file))
        # self.response.write(json.dumps(feed_in, sort_keys=True, indent=4, separators=(',', ': ')))
        out_args = dict(
            title=u'',
            link=u'',
            description=u'',
            feed_url=self.request.url,
        )
        for in_key, in_value in feed_in.iteritems():
            if in_key in ['icon', 'self']:
                pass
            elif in_key == 'entries':
                pass
            else:
                out_args[in_key] = unicode(in_value)

        feed_out = ContentEncodedFeed(**out_args)

        for entry in feed_in['entries']:
            out_args = dict(
                title=u'',
                link=u'',
                description=u'',
            )
            for in_key, in_value in entry.iteritems():
                if in_key in ['author']:
                    for ak, av in in_value.iteritems():
                        out_args[in_key + '_' + ak] = unicode(av)
                elif in_key in ['alternate']:
                    out_args['link'] = out_args['unique_id'] = unicode(in_value)
                elif in_key in ['content']:
                    out_args['description'] = html2text(in_value)
                    out_args['content_encoded'] = unicode(in_value)
                elif in_key in ['published']:
                    out_args['pubdate'] = dateparse.parse_datetime(in_value)
                elif in_key in ['updated']:
                    out_args['updateddate'] = dateparse.parse_datetime(in_value)
                elif in_key in ['categories', 'comments', 'id']:
                    pass
                elif in_key in ['title']:
                    out_args[in_key] = html2text(in_value)
                else:
                    out_args[in_key] = unicode(in_value)
            feed_out.add_item(**out_args)
                
        feed_out.write(self.response, 'utf-8')

#########################################################################################

class ContentEncodedFeed(feedgenerator.Rss201rev2Feed):

    def root_attributes(self):
        attributes = super(ContentEncodedFeed, self).root_attributes()
        attributes['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attributes
        
    def add_item_elements(self, handler, item):
        super(ContentEncodedFeed, self).add_item_elements(handler, item)
        handler.addQuickElement(u'content:encoded', item['content_encoded'])

#########################################################################################

application = webapp2.WSGIApplication([
    webapp2.Route('/facebook/<id:\d+>', handler=FacebookHandler),
], debug=True)
