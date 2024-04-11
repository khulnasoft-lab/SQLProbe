import sys
import urllib
import urllib2
import json
from urlparse import urlparse

from web import useragents

def reverseip(url):
    """Return domains hosted on the same server as the given URL."""
    
    try:
        url_netloc = urlparse(url).netloc if urlparse(url).netloc != '' else urlparse(url).path.split("/")[0]
        source = "http://domains.yougetsignal.com/domains.php"
        useragent = useragents.get()
        contenttype = "application/x-www-form-urlencoded; charset=UTF-8"
        
        # Construct request data
        data = urllib.urlencode([('remoteAddress', url_netloc), ('key', '')])
        
        # Construct request headers
        headers = {
            "Content-type": contenttype,
            "User-Agent": useragent
        }
        
        # Send POST request
        request = urllib2.Request(source, data, headers=headers)
        response = urllib2.urlopen(request)
        result = response.read()
        
        # Parse JSON response
        obj = json.loads(result)
        
        # Check if request was successful
        if obj["status"] == 'Success':
            return [domain[0] for domain in obj["domainArray"]]
        else:
            print >> sys.stderr, "[ERR] {}".format(obj["message"])
            return []
            
    except urllib2.HTTPError as e:
        print >> sys.stderr, "[{}] HTTP error".format(e.code)
        return []
    
    except urllib2.URLError as e:
        print >> sys.stderr, "URL error, {}".format(e.reason)
        return []
    
    except Exception as e:
        print >> sys.stderr, "Error: {}".format(e)
        return []

# Example usage:
# domains = reverseip("example.com")
# print(domains)
