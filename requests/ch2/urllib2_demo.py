# _*_ coding: utf-8 _*_

import urllib2
import urllib

url = 'http://httpbin.org/get'


def use_params_urllib2():
    # user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
    # headers = {'User-Agent': user_agent}
    values = {'name': 'Michael foord',
              'location': 'Nothpton',
              'language': 'Python'}
    params = urllib.urlencode(values)
    req = urllib2.Request(url, params)
    print req
    response = urllib2.urlopen(req)
    print '>>>Response Headers:'
    print response.info()
    print '>>>Status Code:'
    print response.getcode()
    print '>>>Request body:'
    print ''.join([line for line in response.readlines()])


if __name__ == '__main__':
    print '>>>Use params urllib2:'
    use_params_urllib2()
