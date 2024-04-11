import urllib2
from urlparse import urlparse

import useragents


def gethtml(url, last_url=False):
    """Retrieve the HTML content of the given URL."""
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://" + url

    headers = useragents.get()
    request = urllib2.Request(url, headers=headers)
    html = None

    try:
        reply = urllib2.urlopen(request, timeout=10)
        html = reply.read()

    except urllib2.HTTPError as e:
        if e.code == 500:
            # HTTP 500 error, still read HTML content
            html = e.read()
            # Log or handle the error as needed

    except urllib2.URLError as e:
        # Handle URL-related errors
        # Log or handle the error as needed

    except urllib2.socket.timeout:
        # Handle timeout exceptions
        # Log or handle the error as needed

    except KeyboardInterrupt:
        # Allow keyboard interrupts
        raise KeyboardInterrupt

    except Exception as e:
        # Handle other exceptions
        # Log or handle the error as needed

    if html:
        if last_url:
            return html, reply.url
        else:
            return html

    return None
