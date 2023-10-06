import logging
from urllib.parse import urlparse,urljoin
import requests
from crawler_context import Context

from html.parser import HTMLParser
import time



class HTMLLinkParser(HTMLParser):

    urls_extracted = []

    def handle_starttag(self, tag, attrs) -> None:
        if tag == 'a':
            for (attr, value) in attrs:
                if attr == 'href':
                    self.urls_extracted.append(value)
                    break

def extract_urls(context : Context, url: str) -> list[str]:

    try:
        if not context.robot_file_parser.can_fetch(context.robot_parser_agent_name, url):
            context.robot_restricted_urls.add(url)
            logging.debug(f"URL restricted due to robots.txt restriction : {url}")
            return []
        contents = requests.get(url).text
        parser = HTMLLinkParser()
        parser.feed(contents)
        return parser.urls_extracted
    except Exception as e:
        logging.exception(f"Error in fetching URL - {url}")
        context.failed_urls[url] = str(e)
        return []

def get_url_domain(url : str):
    return urlparse(url).netloc

def crawl_urls(context : Context):

    while context.urls_to_visit.qsize() != 0:

        url_to_visit = context.urls_to_visit.get()

        logging.debug(f"Crawling URL = {url_to_visit}")
        logging.debug(f"URLs left to crawl  = {context.urls_to_visit.qsize()}")
        logging.debug(f"Number of Visited URls = {len(context.visited_urls)}")

        if len(context.visited_urls) % 15 == 0:
            logging.debug("Sleeping for 2 seconds")
            logging.info(f"URLs left to crawl  = {context.urls_to_visit.qsize()}")
            logging.info(f"Number of Visited URls = {len(context.visited_urls)}")
            time.sleep(2)

        urls_extracted = extract_urls(context, url_to_visit)

        if urls_extracted is None:
            continue
        context.crawl_results[url_to_visit] = set(urls_extracted)

        context.visited_urls.add(url_to_visit)

        if  context.max_urls is not None and (context.visited_urls >= context.max_urls):
            logging.info("Stopping early as we crawled maximum urls limit set in parameters - {context.max_urls}")
            break

        for url in urls_extracted:
            url_domain = get_url_domain(url)

            if url_domain != context.domain:
                continue
            if url in context.visited_urls or url in context.urls_to_visit.queue:
                continue
            logging.debug(f"Adding URL to visit : {url}")
            context.urls_to_visit.put(url)
        
        context.urls_to_visit.task_done()
        






