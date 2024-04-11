import time
import signal
import multiprocessing
from urllib.parse import urlparse

import std
import sqlerrors
from web import web


def init():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def scan(urls):
    """Scan multiple websites for SQL injection vulnerabilities using multiprocessing."""
    
    vulnerables = []
    results = {}  # Store scanned results

    childs = []  # Store child processes
    max_processes = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(max_processes, init)

    try:
        for url in urls:
            childs.append(pool.apply_async(__sqli, (url, ), callback=__sqli_callback(results, url)))
        
        while not all([child.ready() for child in childs]):
            time.sleep(0.5)
    except KeyboardInterrupt:
        std.stderr("Stopping SQLi scanning process due to keyboard interrupt")
        pool.terminate()
    else:
        pool.close()
    finally:
        pool.join()

    for url, result in results.items():
        if result[0] is True:
            vulnerables.append((url, result[1]))

    return vulnerables

def __sqli_callback(results, url):
    """Returns a callback function to update the results dictionary."""
    
    def callback(result):
        results[url] = result
    return callback

def __sqli(url):
    """Check SQL injection vulnerability for a single URL."""

    std.stdout(f"Scanning {url}", end="")
    domain = url.split("?")[0]  # Domain with path without queries
    queries = urlparse(url).query.split("&")
    
    # No queries in URL
    if not any(queries):
        print("")  # Move cursor to new line
        return False, None

    payloads = ("'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C")
    for payload in payloads:
        website = domain + "?" + ("&".join([param + payload for param in queries]))
        source = web.gethtml(website)
        if source:
            vulnerable, db = sqlerrors.check(source)
            if vulnerable and db is not None:
                std.showsign(" vulnerable")
                return True, db

    print("")  # Move cursor to new line
    return False, None
