import urllib, urllib2
import simplejson

APPID = "RzRkxHvV34Ej1d2DFl.je2afuqgpGxqDh3DW0EMLjl_zUl7NXxmlot.SkPXGPk3I6g--"
SEARCH_URL = "http://boss.yahooapis.com/ysearch/web/v1/"


def yapi(term):
    params = {'appid': APPID, 'format': 'json'}
    url = "%s%s?%s" % (SEARCH_URL, urllib.quote(term.encode("utf-8")), urllib.urlencode(params))
    result = simplejson.loads(urllib2.urlopen(url).read())
    count = float(result['ysearchresponse']['totalhits'])
    return count

