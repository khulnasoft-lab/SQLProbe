import time
import signal
import multiprocessing
from urlparse import urlparse

import std
import sqlerrors
from web import web

def init():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def scan(urls):
    """Scan multiple websites for SQL injection vulnerabilities using multiprocessing."""

    vulnerables = []
    results = {}  # store scanned results

    childs = []  # store child processes
    max_processes = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(max_processes, init)

    for url in urls:
        def callback(result, url=url):
            results[url] = result
        childs.append(pool.apply_async(__sqli, (url, ), callback=callback))

    try:
        while True:
            time.sleep(0.5)
            if all([child.ready() for child in childs]):
                break
    except KeyboardInterrupt:
        std.stderr("Stopping SQLi scanning process")
        pool.terminate()
        pool.join()
    else:
        pool.close()
        pool.join()

    for url, result in results.items():
        if result[0] == True:
            vulnerables.append((url, result[1]))

    return vulnerables

def __sqli(url):
    """Check SQL injection vulnerability for a given URL."""

    std.stdout("Scanning {}".format(url), end="")

    domain = url.split("?")[0]  # domain with path without queries
    queries = urlparse(url).query.split("&")
    # no queries in URL
    if not any(queries):
        print "" # move cursor to new line
        return False, None

    payloads = ("'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C")
    for payload in payloads:
        website = domain + "?" + ("&".join([param + payload for param in queries]))
        source = web.gethtml(website)
        if source:
            vulnerable, db = sqlerrors.check(source)
            if vulnerable and db is not None:
                std.showsign(" Vulnerable")
                return True, db

    print ""  # move cursor to new line
    return False, None

if __name__ == "__main__":
    # Example usage:
    urls_to_scan = ['example.com/page?id=1', 'example.net/login?username=admin']
    results = scan(urls_to_scan)
    print(results)
