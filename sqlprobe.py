import argparse
from urllib.parse import urlparse

from src import std
from src import scanner
from src import reverseip
from src import serverinfo
from src.web import search
from src.crawler import Crawler


# search engine instance
bing = search.Bing()
google = search.Google()
yahoo = search.Yahoo()

# crawler instance
crawler = Crawler()


def singlescan(url):
    """Instance to scan single targeted domain"""

    if urlparse(url).query != '':
        result = scanner.scan([url])
        if result:
            # Scanner.scan() prints if vulnerable
            # therefore exit
            return result
        else:
            print("")  # Move cursor to new line
            std.stdout("No SQL injection vulnerability found")
            option = std.stdin("Do you want to crawl and continue scanning? [Y/N]", ["Y", "N"], upper=True)

            if option == 'N':
                return False

    # Crawl and scan the links
    # If crawl cannot find links, do some reverse domain
    std.stdout("Going to crawl {}".format(url))
    urls = crawler.crawl(url)

    if not urls:
        std.stdout("Found no suitable URLs to test SQLi")
        # std.stdout("You might want to do reverse domain")
        return False

    std.stdout("Found {} URLs from crawling".format(len(urls)))
    vulnerables = scanner.scan(urls)

    if not vulnerables:
        std.stdout("No SQL injection vulnerability found")
        return False

    return vulnerables


def init_parser():
    """Initialize parser arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="dork", help="SQL injection dork", type=str, metavar="inurl:example")
    parser.add_argument("-e", dest="engine", help="search engine [Bing, Google, and Yahoo]", type=str, metavar="bing, google, yahoo")
    parser.add_argument("-p", dest="page", help="number of websites to look for in search engine", type=int, default=10, metavar="100")
    parser.add_argument("-t", dest="target", help="scan target website", type=str, metavar="www.example.com")
    parser.add_argument('-r', dest="reverse", help="reverse domain", action='store_true')
    parser.add_argument('-o', dest="output", help="output result into json", type=str, metavar="result.json")
    parser.add_argument('-s', action='store_true', help="output search even if there are no results")
    return parser


def main():
    parser = init_parser()
    args = parser.parse_args()

    # Find random SQLi by dork
    if args.dork and args.engine:
        std.stdout("Searching for websites with given dork")

        # Get websites based on search engine
        if args.engine in ["bing", "google", "yahoo"]:
            websites = getattr(search, args.engine.capitalize()).search(args.dork, args.page)
        else:
            std.stderr("Invalid search engine")
            exit(1)

        std.stdout("{} websites found".format(len(websites)))

        vulnerables = scanner.scan(websites)

        if not vulnerables:
            if args.s:
                std.stdout("Saved as searches.txt")
                std.dump(websites, "searches.txt")

            exit(0)

        std.stdout("Scanning server information")

        vulnerable_urls = [result[0] for result in vulnerables]
        table_data = serverinfo.check(vulnerable_urls)
        # Add DB name to info
        for result, info in zip(vulnerables, table_data):
            info.insert(1, result[1])  # Database name

        std.fullprint(table_data)

    # Do reverse domain of given site
    elif args.target and args.reverse:
        std.stdout("Finding domains with same server as {}".format(args.target))
        domains = reverseip.reverseip(args.target)

        if not domains:
            std.stdout("No domain found with reversing IP")
            exit(0)

        # If there are domains
        std.stdout("Found {} websites".format(len(domains)))

        # Ask whether user wants to save domains
        std.stdout("Scanning multiple websites with crawling will take long")
        option = std.stdin("Do you want to save domains? [Y/N]", ["Y", "N"], upper=True)

        if option == 'Y':
            std.stdout("Saved as domains.txt")
            std.dump(domains, "domains.txt")

        # Ask whether user wants to crawl one by one or exit
        option = std.stdin("Do you want start crawling? [Y/N]", ["Y", "N"], upper=True)

        if option == 'N':
            exit(0)

        vulnerables = []
        for domain in domains:
            vulnerables_temp = singlescan(domain)
            if vulnerables_temp:
                vulnerables += vulnerables_temp

        std.stdout("Finished scanning all reverse domains")
        if not vulnerables:
            std.stdout("No vulnerable websites from reverse domains")
            exit(0)

        std.stdout("Scanning server information")

        vulnerable_urls = [result[0] for result in vulnerables]
        table_data = serverinfo.check(vulnerable_urls)
        # Add DB name to info
        for result, info in zip(vulnerables, table_data):
            info.insert(1, result[1])  # Database name

        std.fullprint(table_data)

    # Scan SQLi of given site
    elif args.target:
        vulnerables = singlescan(args.target)

        if not vulnerables:
            exit(0)

        # Show domain information of target URLs
        std.stdout("Getting server info of domains can take a few minutes")
        table_data = serverinfo.check([args.target])

        std.printserverinfo(table_data)
        print("")  # Give space between two table
        std.normalprint(vulnerables)
        exit(0)

    # Print help message, if no parameter is provided
    else:
        parser.print_help()

    # Dump result into JSON if specified
    if args.output:
        std.dumpjson(table_data, args.output)
        std.stdout("Dumped result into %s" % args.output)


if __name__ == "__main__":
    main()
