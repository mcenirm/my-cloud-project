import webapp2
import urllib2
import json
from django.utils import feedgenerator, dateparse
from html2text import html2text

#########################################################################################

class FacebookHandler(webapp2.RequestHandler):

    def get(self, id):

        feed_url = 'https://www.facebook.com/feeds/page.php?id=' + id + '&format=json'
        feed_response = urllib2.urlopen(feed_url)

        for header_name in [
            'Expires',
            'Last-Modified',
            'Pragma',
            'Cache-Control',
        ]:
            self.response.headers[header_name] = feed_response.headers[header_name.lower()]
        self.response.headers['Content-Type'] = 'application/rss+xml'

        feed_in = json.load(feed_response)

        feed_out_args = dict(
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
                feed_out_args[in_key] = unicode(in_value)

        feed_out = ContentEncodedFeed(**feed_out_args)

        for entry in feed_in['entries']:
            entry_out_args = dict(
                title=u'',
                link=u'',
                description=u'',
            )
            for in_key, in_value in entry.iteritems():
                if in_key in ['author']:
                    for ak, av in in_value.iteritems():
                        entry_out_args[in_key + '_' + ak] = unicode(av)
                elif in_key in ['alternate']:
                    entry_out_args['link'] = entry_out_args['unique_id'] = unicode(in_value)
                elif in_key in ['content']:
                    entry_out_args['description'] = html2text(in_value)
                    entry_out_args['content_encoded'] = unicode(in_value)
                elif in_key in ['published']:
                    entry_out_args['pubdate'] = dateparse.parse_datetime(in_value)
                elif in_key in ['updated']:
                    entry_out_args['updateddate'] = dateparse.parse_datetime(in_value)
                elif in_key in ['categories', 'comments', 'id']:
                    pass
                elif in_key in ['title']:
                    entry_out_args[in_key] = html2text(in_value)
                else:
                    entry_out_args[in_key] = unicode(in_value)
            feed_out.add_item(**entry_out_args)

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
