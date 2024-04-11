class Search:
    """Basic search class that can be inherited by other search agents like Google, Yandex."""

    def search(self, query, pages=10):
        """Search for vulnerabilities based on the provided query.

        Args:
            query (str): The search query to be used.
            pages (int): The number of search result pages to retrieve. Defaults to 10.

        Returns:
            list: A list of URLs containing potential vulnerabilities.
        """
        raise NotImplementedError("Subclasses must implement the search method.")


class Google(Search):
    def search(self, query, pages=10):
        """Search for vulnerabilities on Google.

        Args:
            query (str): The search query to be used.
            pages (int): The number of search result pages to retrieve. Defaults to 10.

        Returns:
            list: A list of URLs containing potential vulnerabilities.
        """
        try:
            return google.search(query, start=0, stop=pages)
        except (HTTPError, URLError) as e:
            self._handle_error(e)

    def _handle_error(self, error):
        """Handle HTTP or URL errors raised during the search."""
        if isinstance(error, HTTPError):
            exit("[503] Service Unreachable")
        elif isinstance(error, URLError):
            exit("[504] Gateway Timeout")
        else:
            exit("Unknown error occurred")
