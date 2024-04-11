import re
import logging
from urlparse import urlparse
from nyawc.Options import Options
from nyawc.Crawler import Crawler as NyawcCrawler
from nyawc.CrawlerActions import CrawlerActions
from nyawc.http.Request import Request

class Crawler:
    def __init__(self):
        self.links = []
        self.crawler = None
        self.set_options()

    def crawl(self, url):
        if self.crawler is None:
            logging.error("Crawler is not set up")
            return []

        parsed_url = urlparse(url)
        domain = parsed_url.scheme + "://" + parsed_url.netloc

        self.links = []
        self.crawler.start_with(Request(domain))
        return self.links

    def set_options(self, depth=1):
        """Set options for the crawler."""
        options = Options()
        options.scope.max_depth = depth
        options.callbacks.crawler_before_start = self.crawler_start
        options.callbacks.crawler_after_finish = self.crawler_finish
        options.callbacks.request_before_start = self.request_start
        options.callbacks.request_after_finish = self.request_finish

        self.crawler = NyawcCrawler(options)

    def crawler_start(self):
        """Called before the crawler starts crawling."""
        pass

    def crawler_finish(self, queue):
        """Called after the crawler finishes crawling."""
        pass

    def request_start(self, queue, queue_item):
        """Called before the crawler starts a new request."""
        return CrawlerActions.DO_CONTINUE_CRAWLING

    def request_finish(self, queue, queue_item, new_queue_items):
        """Called after the crawler finishes a request."""
        url = queue_item.request.url
        if re.search('(.*?)(.php\?|.asp\?|.apsx\?|.jsp\?)(.*?)=(.*?)', url):
            if url not in self.links:
                self.links.append(url)
        return CrawlerActions.DO_CONTINUE_CRAWLING
